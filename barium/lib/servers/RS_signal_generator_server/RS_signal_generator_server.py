# Copyright (C) 2023 Zach Wall

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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""
### BEGIN NODE INFO
[info]
name = rs_signal_generator
version = 1.3
description = 
instancename = rs_signal_generator


[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 5
### END NODE INFO
"""

from labrad.types import Value
from labrad.devices import DeviceServer, DeviceWrapper
from labrad.server import setting
from twisted.internet.defer import inlineCallbacks, returnValue

TIMEOUT = Value(1, 's')

class RS_wrapper(DeviceWrapper):
    
    @inlineCallbacks
    def connect(self, server, port):
        """Connect to a UCLA rhode and schwarz SML02 controller."""
        print('connecting to "%s" on port "%s"...' % (server.name, port),)
        self.server = server
        self.ctx = server.context()
        self.port = port
        p = self.packet()
        p.open(port)
        p.baudrate(9600)
        p.timeout(TIMEOUT)
        p.read()  # clear out the read buffer 
        yield p.send()


    def packet(self):
        """Create a packet in our private context."""
        return self.server.packet(context=self.ctx)

    def shutdown(self):
        """Disconnect from the serial port when we shut down."""
        return self.packet().close().send()

    @inlineCallbacks
    def write(self, code):
        yield self.packet().write(code).send()

    @inlineCallbacks
    def query(self, code):
        """ Write, then read. """
        p = self.packet()
        p.write(code)
        p.read_line()
        ans = yield p.send()
        return(ans.read_line)
        
    @inlineCallbacks       
    def read(self):
        p = self.packet()
        p.read_line()
        ans = yield p.send()
        return(ans.read_line)
        
class RS_server(DeviceServer):
    name = 'rs_signal_generator'
    deviceWrapper = RS_wrapper


    @inlineCallbacks
    def initServer(self):
        self.current_state = {}
        print('loading config info...',)
        self.reg = self.client.registry()
        self.freq = 32
        self.out = False
        self.level = -5
        yield self.loadConfigInfo()
        yield DeviceServer.initServer(self)

    @inlineCallbacks
    def loadConfigInfo(self):
        """Load configuration information from the registry."""
        reg = self.reg
        yield reg.cd(['', 'Servers', 'rs_signal_generator', 'Links'], True)
        dirs, keys = yield reg.dir()
        p = reg.packet() 
        for k in keys:
            p.get(k, key=k)
        ans = yield p.send()
        self.serialLinks = dict((k, ans[k]) for k in keys)


    @inlineCallbacks
    def findDevices(self):
        """Find available devices from list stored in the registry."""
        devs = []
        for name, (serServer, port) in self.serialLinks.items():    
            if serServer not in self.client.servers:
                continue
            server = self.client[serServer]
            ports = yield server.list_serial_ports()
            if port not in ports:
                continue
            devName = '%s - %s' % (serServer, port)
            devs += [(devName, (server, port))]
        returnValue(devs)



    @setting(100, value='b')       
    def set_output(self, c, value):
        '''
        Sets the output state
        '''
        self.out = value
        dev = self.selectDevice(c)
        if value:
            yield dev.write('OUTPUT ON\n')
        else:
            yield dev.write('OUTPUT OFF\n')
        
    @setting(110, value='v')
    def set_frequency(self, c, value):
        '''
        Sets the frequency
        '''
        if value < .009 or value > 3000:
            return("frequency out of range")
        self.freq = value
        dev = self.selectDevice(c)
        yield dev.write('FREQUENCY ' + str(value) + ' MHz\n')
        
    @setting(120, value='v')
    def set_level(self, c, value):
        '''
        Sets the power
        '''
        if value < -100 or value > 8:
            return("power out of range")
        self.level = value
        dev = self.selectDevice(c)
        yield dev.write('POWER ' + str(value) + '\n')

    @setting(200, returns='s')
    def read_frequency(self, c):
        '''
        reads the frequency
        '''
        dev = self.selectDevice(c)  # selects the device assigned to the client
        h = yield dev.query('FREQ?\n')  # querys command to the device
        return(h)

        
    @setting(300, returns='v')
    def get_frequency(self, c):
        '''
        gets the frequency
        '''
        return(self.freq)

    @setting(310, returns='v')
    def get_level(self, c):
        '''
        gets the frequency
        '''
        return(self.level)

    @setting(320, returns='b')
    def get_state(self, c):
        '''
        gets the frequency
        '''
        return(self.out)
    
if __name__ == "__main__":
    from labrad import util
    util.runServer(RS_server())
