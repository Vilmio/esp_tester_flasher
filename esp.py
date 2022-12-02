import esptool
import time
import os
import subprocess
import json
import RPi.GPIO as GPIO

class Esp:

    def __init__(self) -> None:
        OFF : int = 0
        self.stopped = False
        self.baudrate = 921600
        self.status = "Inactive"
        self.firmwareVersion = self.get_fimrwareVersion()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.gpioHandler(state=OFF)


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
        self.gpioHandler(state=1)
        
        try:
            self.status = "Upload new firmware, please wait!"
            esptool.main(["--chip", "auto", "-b", "{}".format(self.baudrate), "write_flash", "-e","-z","0x1000","firmware_2.10.bin"])
            print("Flash success!")
            self.status =  "ok"
        except Exception as e:
            self.status = "{}".format(e)
        self.gpioHandler(state=0)

    def start_testing(self):
        try:
            print("start testing")
            self.gpioHandler(state=2)
            p = subprocess.Popen("ampy --port /dev/cu.usbserial-0001 get test_report.txt", stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()
            output = output.decode('utf8').replace("'", '"')
            output = output.replace("\n","<br>")
            print(output)
            return output
        except Exception as e:
            print(e)
        self.gpioHandler(state=0)
        #print("Command exit status/return code : ", p_status)

    def gpioHandler(self, state = 0):
        esp = 23
        boot = 22
        if state == 0:
            GPIO.setup(boot, GPIO.OUT)
            GPIO.output(boot, False)
            GPIO.setup(esp, GPIO.OUT)
            GPIO.output(esp, False)
            time.sleep(0.2)
        elif state == 1:
            GPIO.setup(boot, GPIO.OUT)
            GPIO.output(boot, True)
            time.sleep(0.2)
            GPIO.setup(esp, GPIO.OUT)
            GPIO.output(esp, True)
            time.sleep(0.2)
        elif state == 2:
            GPIO.setup(boot, GPIO.OUT)
            GPIO.output(boot, False)
            time.sleep(0.2)
            GPIO.setup(esp, GPIO.OUT)
            GPIO.output(esp, True)
            time.sleep(0.2)