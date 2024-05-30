
import time
import pyvisa
import ftplib


def getFile(ftp, filename):
    try:
        ftp.retrbinary("RETR " + filename, open(filename, "wb").write)
    except:
        print("Error")


def load_latest_image_from_devce():
    ftp = ftplib.FTP("192.168.1.55")
    ftp.login("rigol", "rigol")
    getFile(ftp, "latest.png")



rm = pyvisa.ResourceManager()

scope: pyvisa.resources.Resource = rm.open_resource("TCPIP::192.168.1.55::INSTR")

# 存图
scope.write(":SAVE:IMAGe C:\\latest.png")
time.sleep(10)
load_latest_image_from_devce()
