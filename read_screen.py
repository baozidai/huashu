from pprint import pprint
import pyvisa
import numpy as np
import matplotlib.pyplot as plt


rm = pyvisa.ResourceManager()

scope:pyvisa.resources.Resource = rm.open_resource('TCPIP::192.168.1.55::INSTR')

# 设置读取模式
scope.write(":WAV:SOUR CHAN1")
scope.write(":WAVeform:mode normal") # 读取屏幕上的数据
scope.write(":WAVeform:form ascii")
scope.write(":WAVeform:POINts 1000") # mode 为normal的时候这个值会被忽略

# 查询X上两点时间间隔
scope.write(":WAVeform:XINCrement?")
time_interval=float(scope.read())

# 读取
scope.write(":WAVeform:data?")
data=scope.read()
metadata_ascii = data[:12]
wave_data_ascii = data[12:]
wave_data=wave_data_ascii.split(",")
wave_data.pop()
y_data = np.array(wave_data,dtype="float32")
# 对y_data进行滤波


# 创建一个时间数组，假设每个点之间的时间间隔是恒定的
# 这里我们假设采样率为1000点/秒，并且波形长度为num_points
sampling_rate = 1000  # 采样率，单位：点/秒
time_data = np.arange(0, len(wave_data)) / (1/time_interval)  # 时间数组，单位：秒
print(y_data)
print(time_data)

# 使用matplotlib绘制波形图
plt.figure(figsize=(10, 5))
plt.plot(time_data, y_data, label='Oscilloscope Trace')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (V)')
plt.title('Oscilloscope Waveform')
plt.grid(True)
plt.legend()
plt.show()
