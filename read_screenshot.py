import io
import math
import pyvisa
import numpy as np
from PIL import Image

from PIL import Image
import io
import struct

from PIL import Image
import io
import struct
import math

def float_to_int_with_nan(value):
    if math.isnan(value):
        return 0x7FF8000000000000
    scaled_value = value * 1e9  # 缩放浮点数
    return int(scaled_value)

def display_bmp_from_float_list(float_list, width, height):
    # 将浮点数列表转换为RGB像素值列表
    rgb_values = []
    for value in float_list:
        if math.isnan(value):
            rgb_values.append((255, 255, 255))  # 如果是NaN，设置为白色
        else:
            # 将浮点数缩放到0到255的范围内
            scaled_value = max(0, min(255, int(value * 255)))
            rgb_values.append((scaled_value, scaled_value, scaled_value))

    # 使用PIL库创建BMP图像
    image = Image.new('RGB', (width, height))
    image.putdata(rgb_values)

    # 显示图像
    image.show()

# 假设图像的宽度和高度为100x100像素
width = 100
height = 100

# 假设你知道图像的宽度和高度
width = 1024
height = 630

rm = pyvisa.ResourceManager()

scope = rm.open_resource('TCPIP::192.168.1.55::INSTR')

# 设置读取模式
scope.write(":DISPlay:DATA?")
data=scope.read_binary_values()
print(len(data))
with open("data.txt","w") as file:
    file.write(str(data))
display_bmp_from_float_list(data,width,height)