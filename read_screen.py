from pprint import pprint
import pyvisa
import numpy as np
import matplotlib.pyplot as plt


rm = pyvisa.ResourceManager()

scope:pyvisa.resources.Resource = rm.open_resource('TCPIP::192.168.1.55::INSTR')

# 设置读取模式
scope.write(":WAV:SOUR CHAN1")
scope.write(":WAVeform:mode normal")
scope.write(":WAVeform:form ascii")

# 读取
scope.write(":WAVeform:data?")
data=scope.read()
data=data.split(",")
data.pop()
y_data = np.array(data)
# 对y_data进行滤波


# 创建一个时间数组，假设每个点之间的时间间隔是恒定的
# 这里我们假设采样率为1000点/秒，并且波形长度为num_points
sampling_rate = 1000  # 采样率，单位：点/秒
time_data = np.arange(0, 1000) / sampling_rate  # 时间数组，单位：秒
print(y_data)
print(time_data)

# 使用matplotlib绘制波形图
plt.figure(figsize=(10, 5))
plt.plot(time_data, y_data, label='Oscilloscope Trace')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (Units)')
plt.title('Oscilloscope Waveform')
plt.grid(True)
plt.legend()
plt.show()
