from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# 创建设备标识
identity = ModbusDeviceIdentification()
identity.VendorName = 'Pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
identity.ProductName = 'Pymodbus Server'
identity.ModelName = 'Pymodbus Server'
identity.MajorMinorRevision = '1.0'

# 初始化保持寄存器，从地址0开始，初值为0
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*4),
    co=ModbusSequentialDataBlock(0, [0]*4),
    hr=ModbusSequentialDataBlock(0, [0]*4),
    ir=ModbusSequentialDataBlock(0, [0]*4))

context = ModbusServerContext(slaves=store, single=True)

# 启动服务器
StartTcpServer(context, identity=identity, address=("localhost", 5020))

