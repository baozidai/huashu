import datetime
import os
import shutil
import tkinter as tk
import time
from tkinter import filedialog
import types
import pyvisa
import ftplib
from pymodbus.client import ModbusTcpClient

def get_bus():
    global devices
    return devices.get('bus')
def set_bus(bus):
    global devices
    devices["bus"]=bus
def get_scope():
    global devices
    return devices.get("scope")
def set_scope(scope):
    global devices
    devices["scope"]=scope

def getFile(ftp, filename):
    try:
        ftp.retrbinary("RETR " + filename, open(filename, "wb").write)
        os.rename(filename,"{}.png".format(time.strftime("%Y-%m-%d-%H-%M-%S")))
    except:
        print("Error")


def load_latest_image_from_devce():
    global config
    scope_ip=config["scope_ip"]
    print(config)
    print(scope_ip)
    ftp = ftplib.FTP(scope_ip)
    ftp.login("rigol", "rigol")
    getFile(ftp, "latest.png")


def save_image():
    # 存图
    scope = get_scope()
    scope.write(":SAVE:IMAGe C:\\latest.png")
    time.sleep(10)
    load_latest_image_from_devce()
    image_path = "latest.png"
    filename = os.path.basename("latest.png")
    destination_path = os.path.join(directory, filename)
    shutil.copy(image_path, destination_path)
    write_msg(None,"Image Saved.")


def s_reset():
    """停止并清屏
    """
    get_scope().write(":stop")
    get_scope().write(":clear")
    write_msg(None,"Clear Screen.")
    write_msg(None,"Scope Stopped.")

def cls():
    get_scope().write(":clear")
    write_msg(None,"Clear Screen.")

def read_next_operation():
    global devices
    regs = []
    bus:ModbusTcpClient=devices["bus"]
    for addr in range(40000,40010):
        res=bus.read_input_registers(addr) # 00:清屏 01:启动屏幕更新 02:停止屏幕更新 03:存图片到本机本地
        if not res.isError():
            res_data = res.registers[0]
            regs.append(res_data)
            if res_data == 1 or res_data == "1":
                bus.write_register(addr,0) # 寄存器重置
    idx = None
    if 1 in regs and regs.count(1)==1:
        idx=regs.index(1)
    elif not 1 in regs:
       time.sleep(1) 
    else:
        assert "PLC寄存器置位出错"
    return idx


def bus_check_and_run():
    global start_flag
    if start_flag:
        operations = [
        ":clear",
        ":Run",
        ":stop",
        save_image
    ]
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print("{} 运行中\r".format(current_time),end="")
        op_idx=read_next_operation()
        if op_idx is not None:
            operation = operations[op_idx]
            if type(operation) == str:
                scope = get_scope()
                scope.write(operation)
            elif type(operation) == types.FunctionType:
                operation()
    
    root.after(200, bus_check_and_run)

def scope_run(): 
    get_scope().write(":run")

def scope_stop():
    get_scope().write(":stop")



def start(scope_ip,bus_addr:str,devices:dict):
    global config
    if scope_ip == "":
        scope_ip = "192.168.1.55"
    if bus_addr == "":
        bus_addr = "127.0.0.1:5020"

    config["scope_ip"] = scope_ip
    config["bus_addr"] = bus_addr

    scope_ip = "TCPIP::{}::INSTR".format(scope_ip)
    devices["scope"] = rm.open_resource(scope_ip)
    scope = devices["scope"] 

    ip,port = bus_addr.strip().split(":")
    bus_client = ModbusTcpClient(ip,int(port))
    devices["bus"] = bus_client
    bus_connect_result=bus_client.connect()
    print("bus_connect_result:{}".format(bus_connect_result))

    scope.write(":DISPlay:GRADing:INFinite")
    global start_flag
    start_flag = True



def stop(devices:dict):
    # 当按钮被点击时执行的函数
    global start_flag
    start_flag = False
    devices["scope"].close()
    devices["bus"].close()

def write_msg(lst,msg):
    if lst is None:
        lst = listb
    lst.insert(0,msg)

devices = dict()
config = dict()
start_flag = False
rm = pyvisa.ResourceManager()
scope: pyvisa.resources.Resource = None
print(id(scope))
bus = None
devices["scope"]=scope
devices["bus"]=bus

directory = filedialog.askdirectory()

# 创建主窗口
root = tk.Tk()

# 创建标题标签和输入框1
label1 = tk.Label(root, text="PLC Address with port:")
label1.grid(row=0, column=0)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1)

# 创建标题标签和输入框2
label2 = tk.Label(root, text="Scope IP:")
label2.grid(row=1, column=0)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1)

# 创建两个按钮
button1 = tk.Button(root, text="Start Daemon", command=lambda: start(entry1.get(),entry2.get(),devices))
button1.grid(row=2, column=0)

button2 = tk.Button(root, text="Stop Daemon", command=lambda: stop(devices))
button2.grid(row=2, column=1)

button3 = tk.Button(root, text="Clear Screen", command=lambda: cls())
button3.grid(row=3, column=0)

button_scope_run = tk.Button(root, text="Scope Run", command=lambda: scope_run())
button_scope_run.grid(row=4, column=0)

button_scope_stop = tk.Button(root, text="Scope Stop", command=lambda: scope_stop())
button_scope_stop.grid(row=4, column=1)

button_save_image = tk.Button(root, text="Save image", command=lambda: save_image())
button_save_image.grid(row=5,column=0)

listb  = tk.Listbox(root) 
# button_test = tk.Button(root, text="Test", command=lambda: write_msg(listb,"{}:testaaaaaaaa".format(time.strftime("%D-%H:%M:%S"))))
# button_test.grid(row=6,column=0)

listb.grid(row=6,column=0,columnspan=root.grid_size()[0], sticky="nsew")
root.columnconfigure(0, weight=1)
    
# 重新调度下一次检查（每隔200ms）
root.after(200, bus_check_and_run)

# 运行主循环
root.mainloop()
