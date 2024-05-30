from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("127.0.0.1",port=5020)   # Create client object
client.connect()                           # connect to device, reconnect automatically
# client.write_coil(3, 1, slave=0)        # set information in device
client.write_register(3,3)
# result = client.read_coils(1, 1, slave=0)  # get information from device
result=client.read_input_registers(3)
if not result.isError():
    print(result.registers[0])
client.close()                         # Disconnect device
