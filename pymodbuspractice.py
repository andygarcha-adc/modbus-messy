import clickplus
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('192.168.1.2')       # Create client object
client.connect()                               # connect to device
modbusaddr = clickplus.__addr_translate("TD10")[0]
modbusaddr = 45065


print(modbusaddr)
print('writing...')
client.write_register(modbusaddr, 4003)        # set information in device
print('written complete.')
print('\nreading...')
result = client.read_holding_registers(modbusaddr)  # get information from device
print('read complete.')
print(result.bits[0])                          # use information
client.close()                                 # Disconnect device