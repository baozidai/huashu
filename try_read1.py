import pyvisa
import numpy as np

# 打开VISA资源管理器并找到你的示波器
rm = pyvisa.ResourceManager()
# 假设你的示波器VISA地址是'ASRL1::INSTR'，这通常是通过GPIB、USB或以太网连接的设备的地址
# 你需要根据实际情况修改这个地址
scope = rm.open_resource("TCPIP::192.168.1.55::INSTR")

# 配置示波器以输出ASCII数据（如果需要的话）
# 这取决于你的示波器是否支持ASCII输出以及如何配置它
# scope.write(':FORMAT ASCII')  # 假设这是配置ASCII输出的命令

# 触发示波器以获取新的波形数据
# scope.write('*TRG')  # 假设这是触发示波器的命令

# 等待示波器准备好数据
# 这可能需要一个延迟或者检查示波器的状态
import time

time.sleep(2)  # 等待2秒，这个时间需要根据实际情况调整

# 从示波器获取波形数据
# 假设我们使用'CURV?'命令来获取当前波形的Y值，并且使用'WAVF:POIN?'来获取波形的点数
# 你需要根据你的示波器的手册来确定正确的命令和格式
num_points = int(scope.query("WAVF:POIN?"))  # 获取波形的点数
y_values = scope.query_ascii_values("CURV?")  # 获取波形数据，假设是ASCII格式

# 关闭与示波器的连接
scope.close()

# 现在你有了波形数据，可以将其转换为NumPy数组并进行处理
y_data = np.array(y_values)

# 打印获取到的数据点数量
print(f"Number of data points: {num_points}")

# 打印部分数据以验证
print(y_data[:10])
