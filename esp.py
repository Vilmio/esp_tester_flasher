import esptool
import time
import os
import subprocess
import json


class Esp:

    def __init__(self) -> None:
        self.stopped = False
        self.baudrate = 921600
        self.status = "Inactive"
        self.firmwareVersion = self.get_fimrwareVersion()
        


    def get_fimrwareVersion(self):
        arr = os.listdir()
        for i in arr:
            if i[-3:] == "bin":
                version = i[:-4]
                version = version.split("_")
                return version[1]
        return "0.0"
            
    def start_flash(self):
        print("Start flashing ...")
        
        try:
            self.status = "Upload new firmware, please wait!"
            esptool.main(["--chip", "auto", "-b", "{}".format(self.baudrate), "write_flash", "-e","-z","0x1000","firmware_2.10.bin"])
            print("Flash success!")
            self.status =  "ok"
        except Exception as e:
            self.status = "{}".format(e)

    def start_testing(self):
        try:
            print("start testing")
            p = subprocess.Popen("ampy --port /dev/cu.usbserial-0001 get test_report.txt", stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()
            output = output.decode('utf8').replace("'", '"')
            output = output.replace("\n","<br>")
            print(output)
            
            self.status =  "ok"
            return output
        except Exception as e:
            self.status =  "{}".format(e)