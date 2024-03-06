import labrad

c=labrad.connect()
print(c)
a = c.agilent_33210a_server()
print(a.select_device())

