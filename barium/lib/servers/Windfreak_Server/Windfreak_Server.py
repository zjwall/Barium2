#from common.lib.servers.serialdeviceserver import SerialDeviceServer, setting,\
#inlineCallbacks, SerialDeviceError, SerialConnectionError
#from labrad import types as T
#from twisted.internet.defer import returnValue
#from labrad.support import getNodeName

#SERVERNAME = 'Windfreak Server'
#TIMEOUT = 1.0
#BAUDRATE = 57600

#class Windfreak_Server( SerialDeviceServer ):
#    name = SERVERNAME
#    regKey = 'windfreak' # Not sure what this should be
#    port = None
#    serNode = getNodeName()
#    timeout = T.Value(TIMEOUT,'s')

#    @inlineCallbacks
#    def initServer( self ):
#        if not self.regKey or not self.serNode: raise \
#        SerialDeviceError( 'Must define regKey and serNode attributes' )
#        port = yield self.getPortFromReg( self.regKey )
#        self.port = port
#        try:
#            serStr = yield self.findSerial( self.serNode )
#            self.initSerial( serStr, port, baudrate = BAUDRATE )
#        except SerialConnectionError as e:
#            self.ser = None
#            if e.code == 0:
#                print ('Could not find serial server for node: %s' % \
#                self.serNode)
#                print ('Please start correct serial server')
#            elif e.code == 1:
#                print ('Error opening serial connection')
#                print ('Check set up and restart serial server')
#            else: raise

from labrad.types import Value
from labrad.devices import DeviceServer, DeviceWrapper
from labrad.server import setting
from twisted.internet.defer import inlineCallbacks, returnValue

from labrad.server import LabradServer

class windfreak_wrapper(DeviceWrapper):

    @inlineCallbacks
    def connect(self, server, port):
        """Connect to a Windfreak Device."""
        print('connecting to "%s" on port "%s"...' % (server.name, port),)
        self.server = server
        self.ctx = server.context()
        self.port = port
        p = self.packet()
        p.open(port)
        p.baudrate(38400)
        p.read()  # clear out the read buffer
        p.timeout(TIMEOUT)
        yield p.send()

    def packet(self):
        """Create a packet in our private context."""
        return self.server.packet(context=self.ctx)

    def shutdown(self):
        """Disconnect from the serial port when we shut down."""
        return self.packet().close().send()

    @inlineCallbacks
    def write(self, code):
        """Write a data value to the heat switch."""
        yield self.packet().write(code).send()

    @inlineCallbacks
    def query(self, code):
        """ Write, then read. """
        p = self.packet()
        print("packet")
        p.write_line(code)
        print("wrote")
        
        print("read line", p.read_line())
        #something is wrong around here, personally thinking read_line
        ans = yield p.send()
        print("send")
        returnValue(ans.read_line)
        print("ans")
        
        
##    @inlineCallbacks
##    def read_line(self):
##        """Read the Output from the Device."""
##        print("new read_line")
##        ser = self.getPort(c)
##        print("get Port")
##        message = ser.read()
##        print(message)
##        returnValue(message)
#        p = self.packet()
#        print('packet')
#        p.read_line()
#        print('readline')
#        message = yield p.send()
#        print('sent')
#        print(message.read_line)
#        returnValue(message.read_line)
#        #@setting(170, returns = 's')



class Windfreak_Server(DeviceServer):
    name = 'windfreak'
    deviceWrapper = windfreak_wrapper

    @inlineCallbacks
    def initServer(self):
        self.current_state = {}
        self.frequency = '0'
        self.power = '0'
        self.channel = '?'
        self.onoff = '3'
        print('loading config info...',)
        self.reg = self.client.registry()
        yield self.loadConfigInfo()
        yield DeviceServer.initServer(self)

    @inlineCallbacks
    def loadConfigInfo(self):
        """Load configuration information from the registry."""
        reg = self.reg
        yield reg.cd(['', 'Servers', 'windfreak', 'Links'], True)
        dirs, keys = yield reg.dir()
        p = reg.packet() 
        for k in keys:
            p.get(k, key=k)
        ans = yield p.send()
        self.serialLinks = dict((k, ans[k]) for k in keys)
        # Get output state and last value of current set
        yield reg.cd(['', 'Servers', 'windfreak', 'parameters'], True)
        dirs, keys = yield reg.dir()
        p = reg.packet()
        for k in keys:
            p.get(k, key=k)
        ans = yield p.send()
        self.params = dict((k, ans[k]) for k in keys)
        for key in self.params:
            self.current_state[key] = list(self.params[key])
            
    @inlineCallbacks
    def findDevices(self):
        """Find available devices from list stored in the registry."""
        devs = []
        for name, (serServer, port) in self.serialLinks.items():
            if serServer not in self.client.servers:
                #serServer has to be the Serial Server
                continue
            server = self.client[serServer]
            ports = yield server.list_serial_ports()
            if port not in ports:
                continue
            devName = '%s - %s' % (serServer, port)
            devs += [(devName, (server, port))]
        returnValue(devs)

    @setting(151, channel1 = 'w')
    def set_channel(self, c, channel1):
        """
        Switch between input channels on the Windfreak. 
        Acceptable Range: [0, 1]
        """
        dev = self.selectDevice(c)
        if channel1 > 1 or channel1 < 0:
            returnValue('Channel number needs to be 0 or 1')
        else:
            self.channel = channel1
            print(channel1)
            yield dev.write(str.encode('C' + str(channel1) + '\n'))

    @setting(152, freq = 'v')
    def set_freq(self, c, freq):
        """
        Set the frequency for the Windfreak. The unit is always MHz.
        Acceptable Range: [53.0MHz, 13999.999999MHz].
        Resolution 0.1Hz.
        """
        print('setting freq')
        dev = self.selectDevice(c)
        if freq < 53.0 or freq > 13999.999999:
            returnValue('Frequency must be between 53.0 and 13999.999999MHz.')
        else:
            self.frequency = freq
            print('setting freq2')
            yield dev.write(str.encode('f' + str(freq) + '\n'))

    @setting(153, p = 'v')
    def set_power(self, c, p):
        """
        Set the power for the Windfreak. The unit is always dBm.
        Acceptable Range: [-60.0dBm, 20dBm] depending on the frequency.
        Resolution: 0.001dB.
        With this setting the SynthHD will automatically calibrate itself
        and set the power as close as it can get to what is requested.
        """
        dev = self.selectDevice(c)
        if p < -60.0 or p > 20.:
            returnValue('Power must be between -60.0 and 20dBm.')
        else:
            self.power = p
            yield dev.write(str.encode('W' + str(p) + '\n'))

    @setting(154)
    def set_rf_on(self, c):
        """
        Turn the RF ON for the Windfreak.
        """
        dev = self.selectDevice(c)
        self.onoff = 1
        yield dev.write(str.encode('E1r1' + '\n'))

    @setting(155)
    def set_rf_off(self, c):
        """
        Turn the RF OFF for the Windfreak.
        """
        dev = self.selectDevice(c)
        self.onoff = 0
        yield dev.write(str.encode('E0r0' + '\n'))
        
    @setting(160, returns = 's')
    def get_channel(self, c):
        """
        Return the channel that's currently under control for the Windfreak.
        """
        return(self.channel)#str(self.channel))
##        dev = self.selectDevice(c)
##        #ser = self.getPort(c)
##        print('Selected Device')
##        #yield dev.write('C?\r\n')
##        #message = dev.read(1)
##        message = yield dev.query(str.encode('C?'+ '\n'))#read()
##        print('Input and Output Message')
##        #message = yield dev.read_line()
##        print(message)
##        try:
##            #returnValue(int(message[0]))
##            returnValue(message)
##        except Exception:
##            returnValue("Something went wrong, cannot get current channel")

    @setting(161, returns = 's')
    def get_frequency(self, c):
        """
        Return the frequency that's currently set for the Windfreak.
        """
        return(self.frequency)
##        dev = self.selectDevice(c)
##        # yield dev.write(str.encode('f?' + '\n'))
##        # message = yield dev.read()
##        message = yield dev.query(str.encode('f?'+ '\n'))
##        try:
##            returnValue(message)
##        except Exception:
##            returnValue("Something went wrong, cannot get current frequency")

    @setting(162, returns = 's')
    def get_power(self, c):
        """
        Return the power that's currently set for the Windfreak.
        """
        return(self.power)
##        dev = self.selectDevice(c)
##        # yield dev.write(str.encode('W?' + '\n'))
##        # message = yield dev.read()
##        message = yield dev.query(str.encode('W ?'+ '\n'))
##        try:
##            returnValue(message)
##        except Exception:
##            returnValue("Something went wrong, cannot get current power")


    @setting(163, returns = 's')
    def get_onoff(self, c):
        """
        Return the power that's currently set for the Windfreak.
        """
        onoff = '?'
        if self.onoff == 1:
            onoff = 'ON'
        elif self.onoff == 0:
            onoff = 'OFF'
        return(onoff)
            
TIMEOUT = Value(1, 's')
__server__ = Windfreak_Server()

if __name__ == "__main__":
    from labrad import util
    util.runServer(__server__)


            
