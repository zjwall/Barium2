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
name = wind server
version = 1.3
description = 
instancename = wind server


[startup]
cmdline = %PYTHON% %FILE%
timeout = .1

[shutdown]
message = 987654321
timeout = 5
### END NODE INFO
"""
import os

import socket
from labrad.types import Value
from labrad.devices import DeviceServer, DeviceWrapper
from labrad.server import setting
from twisted.internet.defer import inlineCallbacks, returnValue

TIMEOUT = Value(1, 's')

class wind_wrapper(DeviceWrapper):
    
    @inlineCallbacks
    def connect(self, server, port):
        """Connect to a UCLA windfreak device"""
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
        yield self.packet().write(str(code)).send()

    @inlineCallbacks
    def query(self, code):
        """ Write, then read. """
        p = self.packet()
        p.write(str(code))
        p.read_line()
        ans = yield p.send()
        return(ans.read_line)
        
    @inlineCallbacks       
    def read(self):
        p = self.packet()
        p.read_line()
        ans = yield p.send()
        return(ans.read_line)
        
class wind_server(DeviceServer):
    name = 'wind'
    deviceWrapper = wind_wrapper


    @inlineCallbacks
    def initServer(self):
        self.current_state = {}
        print('loading config info...',)
        self.reg = self.client.registry()
        self.freq = 100
        self.out = False
        self.level = -5
        self.channel = 0
        self.trig = 0
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



    @setting(70, value='b')       
    def set_trigger(self,c, value):
        '''
        Sets the trigger, True means the device expect a trigger, False means the device does not need a trigger and is always on
        '''
        self.trig = value
        dev = self.selectDevice(c)
        if value:
            yield dev.write('w4')
        else:
            yield dev.write('w0')

    @setting(71)       
    def read_trigger(self,c):
        '''
        reads the trigger
        '''
        dev = self.selectDevice(c)
        h = yield dev.query('w?\n')
        self.trig = bool(h)
        return(h)
    
    @setting(80)       
    def set_reference(self,c):
        '''
        Sets the reference
        '''
        dev = self.selectDevice(c)
        yield dev.write('x0')     

    @setting(81)       
    def set_reference_freq(self, c):
        '''
        Sets the reference
        '''
        dev = self.selectDevice(c)
        yield dev.write('*10')
        
    @setting(82)       
    def read_reference_freq(self, c):
        '''
        Sets the reference
        '''
        dev = self.selectDevice(c)
        h = yield dev.query('*?\n')
        self.channel = float(h)
        return(h)
    
            
    @setting(90, value='i')       
    def set_channel(self, c, value):
        '''
        Sets the channel, 0=A, 1=B
        '''
        self.out = value
        dev = self.selectDevice(c)
        if value == 1:
            yield dev.write('C1')
            self.channel = 1
        if value == 0:
            yield dev.write('C0')
            self.channel = 0

    @setting(91)       
    def read_channel(self, c, value):
        '''
        Sets the channel, 0=A, 1=B
        '''
        dev = self.selectDevice(c)
        h = yield dev.query('C?\n')
        self.channel = float(h)
        return(h)

            
    @setting(100, value='b')       
    def set_output(self, c, value):
        '''
        Sets the output state
        '''
        self.out = value
        dev = self.selectDevice(c)
        if value:
            yield dev.write('h1')
        else:
            yield dev.write('h0')

    @setting(101)       
    def read_output(self, c):
        '''
        Sets the output state
        '''
        dev = self.selectDevice(c)
        h = yield dev.query('h?\n')
        self.out = bool(h)
        return(h)

            
    @setting(110, value='v')
    def set_freq(self, c, value):
        '''
        Sets the frequency
        '''
        if value < 53 or value > 13999:
            return("frequency out of range")
        self.freq = value
        dev = self.selectDevice(c)
        yield dev.write('f' + str(value) + '\n')
        
    @setting(200, returns='s')
    def read_freq(self, c):
        '''
        reads the frequency
        '''
        dev = self.selectDevice(c)  # selects the device assigned to the client
        h = yield dev.query('f?\n')  # querys command to the device
        self.freq = float(h)
        return(h)

        
    @setting(120, value='v')
    def set_power(self, c, value):
        '''
        Sets the power
        '''
        if value < -60 or value > 20:
            return("power out of range")
        self.level = value
        dev = self.selectDevice(c)
        yield dev.write('W' + str(value) + '\n')


    @setting(121)
    def read_power(self, c):
        '''
        Sets the power
        '''

        dev = self.selectDevice(c)
        h = yield dev.query('W?\n')
        self.level = float(h)
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
    util.runServer(wind_server())
