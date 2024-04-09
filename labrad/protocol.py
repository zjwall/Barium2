# Copyright (C) 2007  Matthew Neeley
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
labrad.protocol

Defines the sending and receiving of packets on the network,
as well as the protocol for connecting to the Manager and
authenticating.
"""

from __future__ import print_function

from builtins import input

import hashlib
import traceback

from twisted.internet import reactor, protocol, defer
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.python import failure, log

import labrad.types as T
from labrad import auth, constants as C, crypto, errors, oauth, support, util
from labrad.stream import packetStream, flattenPacket


class LabradProtocol(protocol.Protocol):
    """Receive and send labrad packets."""

    def __init__(self):
        self.disconnected = False
        self._next_context = 1
        self._nextRequest = 1
        self.pool = set()
        self.requests = {}
        self.listeners = {}
        self._messageLock = defer.DeferredLock()
        self.clearCache()
        self.endianness = '>'
        self.request_handler = None
        # create a generator to assemble the packets
        self.packetStream = packetStream(self.packetReceived, self.endianness)
        next(self.packetStream) # start the packet stream

        self.onDisconnect = util.DeferredSignal()

    def set_address(self, host, port):
        """Store host and port of remote endpoint in protocol object.

        This is called by the connect function below after successfully
        establishing a connection. The host and port are used to cache our
        credentials after we authenticate successfully.

        Args:
            host (str): The hostname we are connected to.
            port (int): The TCP port number we are connected to.
        """
        self.host = host
        self.port = port

    def context(self):
        """Create a new communication context for this connection."""
        context = (0, self._next_context)
        self._next_context += 1
        return context

    # network events
    def connectionMade(self):
        # set the SO_KEEPALIVE option on all connections
        self.transport.setTcpNoDelay(True)
        self.transport.setTcpKeepAlive(True)

    def connectionLost(self, reason):
        """Called when the network connection is lost.

        This can be due to the disconnect() method being
        called, or because of some network error.
        """
        self.disconnected = True
        for d in list(self.requests.values()):
            d.errback(Exception('Connection lost.'))
        if reason == protocol.connectionDone:
            self.onDisconnect.callback(None)
        else:
            self.onDisconnect.errback(reason)

    def disconnect(self):
        """Close down the connection to LabRAD."""
        self.disconnected = True
        self.transport.loseConnection()

    # sending
    def sendPacket(self, target, context, request, records):
        """Send a raw packet to the specified target."""
        raw = flattenPacket(target, context, request, records, endianness=self.endianness)
        self.transport.write(raw)

    @inlineCallbacks
    def sendMessage(self, target, records, context=(0, 0)):
        """Send a message to the specified target."""
        target, records = yield self._lookupNames(target, records)
        self.sendPacket(target, context, 0, records)

    @inlineCallbacks
    def sendRequest(self, target, records, context=(0, 0), timeout=None, unflatten=True):
        """Send a request to the given target server.

        Returns a deferred that will fire the resulting data packet when
        the request is completed, or will errback if the request times out
        or errors are returned from labrad.  The target server and settings
        may be given either as word IDs or string names.  If necessary,
        any string names will be looked up before the request is sent.
        Lookup results are cached to avoid lookup overhead on subsequent
        requests to the same server or settings.
        """
        target, records = yield self._lookupNames(target, records)
        resp = yield self._sendRequestNoLookup(target, records, context, timeout, unflatten)
        returnValue(resp)

    @inlineCallbacks
    def _lookupNames(self, server, records):
        """Translate server and setting names into IDs.

        We first attempt to look up these names in the local cache.
        If any are not found there, we fire off a request to the
        Manager to lookup the necessary IDs, and then cache the
        result.
        """
        records = list(records)

        # try to lookup server in cache
        if isinstance(server, str) and server in self._serverCache:
            server = self._serverCache[server]

        # try to lookup settings in cache
        if server in self._settingCache:
            settings = self._settingCache[server]
            for i, rec in enumerate(records):
                name = rec[0]
                if isinstance(name, str) and name in settings:
                    records[i] = (settings[name],) + tuple(rec[1:])

        # check to see whether there is still anything to look up
        settingLookups = [(i, rec[0]) for i, rec in enumerate(records)
                                      if isinstance(rec[0], str)]
        if isinstance(server, str) or len(settingLookups):
            # need to do additional lookup here
            if len(settingLookups):
                indices, names = zip(*settingLookups)
            else:
                indices, names = [], []
            # send the actual lookup request
            recs = [(C.LOOKUP, (server, names), ['w*s', 's*s'])]
            resp = yield self._sendRequestNoLookup(C.MANAGER_ID, recs)
            serverID, IDs = resp[0][1]
            # cache the results
            if isinstance(server, str):
                self._serverCache[server] = serverID
            server = serverID
            settings = self._settingCache.setdefault(server, {})
            settings.update(zip(names, IDs))
            # update the records for the packet
            for index, ID in zip(indices, IDs):
                records[index] = (ID,) + tuple(records[index][1:])

        returnValue((server, records))

    def clearCache(self):
        """Clear the cache of looked-up server and settings IDs."""
        self._serverCache = {}
        self._settingCache = {}

    def unflattenResponse(self, response_records):
        return [(ID, data.unflatten()) for (ID, data) in response_records]

    def _sendRequestNoLookup(self, target, records, context=(0, 0), timeout=None, unflatten=True):
        """Send a request without doing any lookups of server or setting IDs."""
        if self.disconnected:
            raise Exception('Already disconnected.')
        if len(self.pool):
            n = self.pool.pop()
        else:
            n = self._nextRequest
            self._nextRequest += 1

        self.requests[n] = d = defer.Deferred()
        if timeout is not None:
            timeoutCall = reactor.callLater(timeout, d.errback,
                                            errors.RequestTimeoutError())
            d.addBoth(self._cancelTimeout, timeoutCall)
        d.addBoth(self._finishRequest, n)
        if unflatten:
            d.addCallback(self.unflattenResponse)
        self.sendPacket(target, context, n, records)
        return d

    @inlineCallbacks
    def _sendManagerRequest(self, setting_id=None, data=None, timeout=None):
        if setting_id is None:
            records = []
        else:
            records = [(setting_id, data)]
        resp = yield self.sendRequest(C.MANAGER_ID, records, timeout=timeout)
        returnValue(resp[0][1])

    def _cancelTimeout(self, result, timeoutCall):
        """Cancel a pending request timeout call."""
        if timeoutCall.active():
            timeoutCall.cancel()
        return result

    def _finishRequest(self, result, n):
        """Finish a request."""
        del self.requests[n]
        self.pool.add(n) # reuse request numbers
        return result                                                

    # receiving
    def dataReceived(self, data):
        self.packetStream.send(data)

    def packetReceived(self, source, context, request, records):
        """Process incoming packet."""
        if request > 0:
            self.requestReceived(source, context, request, records)
        elif request < 0:
            self.responseReceived(source, context, request, records)
        else:
            self.messageReceived(source, context, records)

    @inlineCallbacks
    def requestReceived(self, source, context, request, flat_records):
        """Process incoming request."""
        try:
            if self.request_handler is None:
                log.msg('server request_handler not set')
                raise Exception('server request_handler not set')
            response = yield self.request_handler(source, context, flat_records)
            self.sendPacket(source, context, -request, response)
        except Exception as e:
            # this will only happen if there was a problem while sending,
            # which usually means a problem flattening the response into
            # a valid LabRAD packet
            self.sendPacket(source, context, -request, [(0, e)])

    def responseReceived(self, source, context, request, flat_records):
        """Process incoming response."""
        if -request in self.requests: # reply has request number negated
            d = self.requests[-request]
            errors = [r[1].unflatten() for r in flat_records if isinstance(r[1].tag, T.TError)]
            if errors:
                # fail on the first error
                d.errback(errors[0])
            else:
                d.callback(flat_records)
        else:
            # probably a response for a request that has already
            # timed out.  If not, something bad has happened.
            log.msg('Invalid response: %s, %s, %s, %s' % \
                    (source, context, request, records))

    def messageReceived(self, source, context, flat_records):
        """Process incoming messages."""
        self._messageLock.run(self._dispatchMessage, source, context, flat_records)

    @inlineCallbacks
    def _dispatchMessage(self, source, context, flat_records):
        """Dispatch a message to all matching listeners."""
        for ID, flat_data in flat_records:
            data = flat_data.unflatten()
            msgCtx = MessageContext(source, context, ID)
            keys = ((s, c, i) for s in (source, None)
                              for c in (context, None)
                              for i in (ID, None)
                              if (s, c, i) in self.listeners)
            for key in keys:
                for listener, sync in self.listeners[key]:
                    func, args, kw = listener
                    @inlineCallbacks
                    def call_handler():
                        try:
                            yield func(msgCtx, data, *args, **kw)
                        except Exception:
                            print('Unhandled error in message listener:',
                                  msgCtx, data, listener)
                            traceback.print_exc()
                    d = call_handler()
                    if sync:
                        yield d

    # message handling
    def addListener(self, listener, source=None, context=None, ID=None, sync=False, args=(), kw={}, **kwargs):
        """Add a listener for messages with the specified attributes.

        When a message with the specified source, context and ID is received,
        listener will be called with the message data, along with the args and
        keyword args specified here.  sync determines how message listeners
        that return deferreds are to be handled.  If sync is False, the message
        dispatcher will not wait for the deferred returned by a listener to fire.
        However, if sync is True, the dispatcher will wait for this deferred
        before firing any more messages.
        """
        # this function used to have an async parameter with inverted logic to
        # the current sync parameter. This had to be changed as python 3.7 made
        # async a keyword. This workaround allows to maintain the old API for
        # older python versions.
        if 'async' in kwargs:
            sync = not kwargs['async']

        key = (source, context, ID)
        listeners = self.listeners.setdefault(key, [])
        listeners.append(((listener, args, kw), sync))

    def removeListener(self, listener, source=None, context=None, ID=None):
        """Remove a listener for messages."""
        key = (source, context, ID)
        listeners = [l for l in self.listeners[key] if l[0][0] != listener]
        if len(listeners):
            self.listeners[key] = listeners
        else:
            del self.listeners[key]

    @inlineCallbacks
    def spawn(self, client=True):
        p = yield connect(**self.spawn_kw)
        if client or len(self.ident) == 1:
            yield p.loginClient(self.name)
        else:
            yield p.loginServer(*self.ident)
        returnValue(p)

    @inlineCallbacks
    def authenticate(self, username=None, password=None, headless=False):
        """Authenticate to the manager using the given credentials."""

        @inlineCallbacks
        def get_manager_auth_methods():
            if 'auth-server' in self.manager_features:
                # Ask the manager what auth methods it supports
                methods = yield self._sendManagerRequest(101, None)
            else:
                # Old managers only support password auth
                methods = ['password']
            returnValue(set(methods))

        def require_secure_connection(auth_type):
            is_secure = hasattr(self.transport, 'getPeerCertificate')
            is_local_connection = util.is_local_connection(self.transport)
            if not is_secure and not is_local_connection:
                raise Exception("cannot use {} auth over an insecure remote "
                                "connection".format(auth_type))

        # Get username and password from environment if not passed here
        if username is None:
            username = C.USERNAME
        if password is None:
            cred = auth.get_password(self.host, self.port, username,
                                     prompt=False)
            if cred is not None:
                password = cred.password

        if password is not None or username is not None:
            # Use password-based auth
            if username is None:
                # Have password; assume root user
                credential = auth.Password(password=password)
            elif password is None:
                # Have username; get password from cache or prompt
                credential = auth.get_password(
                        self.host, self.port, user=username, prompt=True)
            else:
                # Have username and password; use both
                if not username:
                    # Empty username is the root user
                    credential = auth.Password(password=password)
                else:
                    # Some other user; make sure manager supports user auth.
                    manager_auth_methods = yield get_manager_auth_methods()
                    if 'username+password' not in manager_auth_methods:
                        raise Exception('Manager does not support '
                                        'username+password auth. Cannot log in '
                                        'as user {}.'.format(username))
                    credential = auth.Password(username, password)

        else:
            # Have neither username nor password.
            # Check manager-supported auth methods; use OAuth if available.
            manager_auth_methods = yield get_manager_auth_methods()
            oauth_methods = {'oauth_token', 'oauth_access_token'}
            client_auth_methods = {'password', 'username+password'} | oauth_methods
            allowed = client_auth_methods & manager_auth_methods

            if oauth_methods & allowed:
                if 'oauth_access_token' in allowed:
                    # Prefer using access token if manager supports it.
                    method = 'oauth_access_token'
                else:
                    method = 'oauth_token'
                auth_info = yield self._sendManagerRequest(102, method)
                auth_info = dict(auth_info)
                credential = oauth.get_token(auth_info['client_id'],
                                             auth_info['client_secret'],
                                             headless=headless)
            elif 'username+password' in allowed:
                credential = auth.get_username_and_password(
                        self.host, self.port, prompt=True)
            else:
                credential = auth.get_password(
                        self.host, self.port, user='', prompt=True)

        if isinstance(credential, auth.Password):
            if not credential.username:
                # send login packet to get password challenge
                challenge = yield self._sendManagerRequest()

                # send password response
                m = hashlib.md5()
                m.update(challenge)
                if isinstance(credential.password, bytes):
                    m.update(credential.password)
                else:
                    m.update(credential.password.encode('UTF-8'))
                try:
                    resp = yield self._sendManagerRequest(0, m.digest())
                except Exception:
                    raise errors.LoginFailedError('Incorrect password.')
            else:
                method = 'username+password'
                require_secure_connection(method)
                try:
                    data = (credential.username, credential.password)
                    resp = yield self._sendManagerRequest(103, (method, data))
                except Exception as e:
                    raise errors.LoginFailedError(str(e))
            auth.cache_password(self.host, self.port, credential)

        elif isinstance(credential, oauth.OAuthToken):
            require_secure_connection(method)
            try:
                if method == 'oauth_access_token':
                    data = credential.access_token
                else:
                    data = credential.id_token
                resp = yield self._sendManagerRequest(103, (method, data))
            except Exception as e:
                raise errors.LoginFailedError(str(e))

        self.credential = credential
        self.loginMessage = resp

    def loginClient(self, name):
        """Log in as a client by sending our name to the manager.

        Args:
            name (str): The name of this labrad connection. Need not be unique.

        Returns:
            twisted.internet.defer.Deferred(None): A deferred that will fire
            after we have logged in.
        """
        return self._doLogin(name)

    def loginServer(self, name, descr, notes):
        """Log in as a server by sending our name and metadata to the manager.

        Args:
            name (str): The name of this server. Must be unique; login will
                fail if another server of the same name is already connected.
            descr (str): A description of this server, which will be exposed
                to other labrad clients.
            notes (str): More descriptive information about the server. This
                field is deprecated; instead we recommend just putting all info
                into descr.

        Returns:
            twisted.internet.defer.Deferred(None): A deferred that will fire
            after we have logged in.
        """
        return self._doLogin(name, descr, notes)

    @inlineCallbacks
    def _doLogin(self, *ident):
        self.ident = ident
        # Store name, which is always the first identification param.
        self.name = ident[0]
        # Send identification.
        data = (1,) + ident
        tag = 'w' + 's'*len(ident)
        flat = T.flatten(data, tag)
        self.ID = yield self._sendManagerRequest(0, flat)


class MessageContext(object):
    """Object to be passed as the first argument to message handlers."""

    def __init__(self, source, context, target):
        self.source = source
        self.ID = context
        self.target = target

    def __repr__(self):
        return 'MessageContext(source=%s, ID=%s, target=%s)' % (self.source, self.ID, self.target)


# factory for creating LabRAD connections
_factory = protocol.ClientCreator(reactor, LabradProtocol)


@inlineCallbacks
def connect(host=C.MANAGER_HOST, port=None, tls_mode=C.MANAGER_TLS,
            username=None, password=None, headless=False):
    """Connect to LabRAD and return a deferred that fires the protocol object.

    Args:
        host (str): The hostname of the manager.
        port (int): The tcp port of the manager. If None, use the appropriate
            default value based on the TLS mode.
        tls_mode (str): The tls mode to use for this connection. See:
            `labrad.constants.check_tls_mode`.
        username (str | None): The username to use when authenticating.
        password (str | None): The password to use when authenticating.
        headless (bool): Whether to use headless OAuth flow if no username or
            password is configured.

    Returns:
        twisted.internet.defer.Deferred(LabradProtocol): A deferred that will
        fire with the protocol once the connection is established.
    """
    spawn_kw = dict(host=host, port=port, tls_mode=tls_mode,
                    username=username, password=password, headless=headless)

    tls_mode = C.check_tls_mode(tls_mode)
    if port is None:
        port = C.MANAGER_PORT_TLS if tls_mode == 'on' else C.MANAGER_PORT

    @inlineCallbacks
    def authenticate(p):
        yield p.authenticate(username, password, headless)

    if tls_mode == 'on':
        tls_options = crypto.tls_options(host)
        p = yield _factory.connectSSL(host, port, tls_options, timeout=C.TIMEOUT)
        p.set_address(host, port)
        p.spawn_kw = spawn_kw
        yield authenticate(p)
        returnValue(p)

    @inlineCallbacks
    def do_connect():
        p = yield _factory.connectTCP(host, port, timeout=C.TIMEOUT)
        p.set_address(host, port)
        p.spawn_kw = spawn_kw
        returnValue(p)

    @inlineCallbacks
    def start_tls(p, cert_string=None):
        try:
            cert = yield p._sendManagerRequest(1, ('STARTTLS', host))
        except Exception:
            raise Exception(
                'Failed sending STARTTLS command to server. You should update '
                'the manager and configure it to support encryption or else '
                'disable encryption for clients. See '
                'https://github.com/labrad/pylabrad/blob/master/CONFIG.md')
        p.transport.startTLS(crypto.tls_options(host, cert_string=cert_string))
        returnValue(cert)

    @inlineCallbacks
    def ping(p):
        resp = yield p._sendManagerRequest(2, 'PING')
        if isinstance(resp, tuple):
            manager_features = set(resp[1])
        else:
            manager_features = set()
        returnValue(manager_features)

    p = yield do_connect()
    is_local_connection = util.is_local_connection(p.transport)
    if ((tls_mode == 'starttls-force') or
        (tls_mode == 'starttls' and not is_local_connection)):
        try:
            cert = yield start_tls(p)
        except Exception:
            # TODO: remove this retry. This is a temporary fix to support
            # compatibility until TLS is fully deployed.
            print('STARTTLS failed; will retry without encryption in case we '
                  'are connecting to a legacy manager.')
            p = yield connect(host, port, tls_mode='off')
            print('Connected without encryption.')
            p.manager_features = set()
            yield authenticate(p)
            returnValue(p)
        try:
            manager_features = yield ping(p)
        except Exception:
            print('STARTTLS failed due to untrusted server certificate:')
            print('SHA1 Fingerprint={}'.format(crypto.fingerprint(cert)))
            print()
            while True:
                ans = input(
                        'Accept server certificate for host "{}"? (accept just '
                        'this [O]nce; [S]ave and always accept this cert; '
                        '[R]eject) '.format(host))
                ans = ans.lower()
                if ans in ['o', 's', 'r']:
                    break
                else:
                    print('Invalid input:', ans)
            if ans == 'r':
                raise
            p = yield do_connect()
            yield start_tls(p, cert)
            manager_features = yield ping(p)
            if ans == 's':
                # save now that we know TLS succeeded,
                # including hostname verification.
                crypto.save_cert(host, cert)
    else:
        manager_features = yield ping(p)
    p.manager_features = manager_features

    yield authenticate(p)
    returnValue(p)
