import esptool
import time
import os
from subprocess import Popen, PIPE
import shlex
import json
from threading import Timer
try:
    import RPi.GPIO as GPIO
except:
    pass
import re

class Esp:

    def __init__(self) -> None:
        OFF : int = 0
        self.AMPY_TIMEOUT = 20
        self.stopped = False
        self.baudrate = 1843200
        self.status = "Inactive"
        self.firmwareVersion = self.get_fimrwareVersion()
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            self.gpioHandler(state=OFF)
        except:
            pass


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
        self.gpioHandler(state=0)
        self.gpioHandler(state=1)
        
        try:
            self.status = "Upload new firmware, please wait!"
            esptool.main(["--chip", "auto", "-b", "{}".format(self.baudrate), "write_flash", "-e","-z","0x1000","firmware_{}.bin".format(self.firmwareVersion)])
            print("Flash success!")
            self.status =  "ok"
        except Exception as e:
            self.status = "{}".format(e)
        
        self.gpioHandler(state=0)

    def Convert(self, lst):
        it = iter(lst)
        res_dct = dict(zip(it, it))
        return res_dct


    def start_testing(self):
        try:
            print("start testing")
            self.gpioHandler(state=0)
            self.gpioHandler(state=2)
            self.run("ampy --port /dev/ttyAMA0 get test_report.txt",self.AMPY_TIMEOUT)
            
            output = output.decode('utf8').replace("'", '"')
            output = output.replace(" ", "")
            res = re.split("[:\n]",output)
            output = self.Convert(res)
            if "EVSE" in output:
                if "OK" in output["EVSE"]:
                    output["EVSE"] = "<span id='success'> OK </span>"
                else:
                    output["EVSE"] = "<span id='fail'> NOK </span>"
            if "WATTMETER" in output:
                if "OK" in output["WATTMETER"]:
                    output["WATTMETER"] = "<span id='success'> OK </span>"
                else:
                    output["WATTMETER"] = "<span id='fail'> NOK </span>"
            if "RELAY" in output:
                if "OK" in output["RELAY"]:
                    output["RELAY"] = "<span id='success'> OK </span>"
                else:
                    output["RELAY"] = "<span id='fail'> NOK </span>"
            if "DE" in output:
                if "OK" in output["DE"]:
                    output["DE"] = "<span id='success'> OK </span>"
                else:
                    output["DE"] = "<span id='fail'> NOK </span>"
            if "Firmwareversion" in output:
                if self.firmwareVersion in output["Firmwareversion"]:
                    output["Firmwareversion"] = "<span id='success'> {} </span>".format(self.firmwareVersion)
                else:
                    output["Firmwareversion"] = "<span id='fail'> NOK </span>"
            else:
                self.status =  "fail"
                self.gpioHandler(state=0)
                return "ESP firmware failed to load. No such file: test_report.txt"

            self.status =  "ok"
            self.gpioHandler(state=0)
            return output
        except Exception as e:
            self.status =  "fail"
            self.gpioHandler(state=0)
            return e
        #print("Command exit status/return code : ", p_status)

    def run(cmd, timeout_sec):
        proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        timer = Timer(timeout_sec, proc.kill)
        stderr = None
        stdout = None
        try:
            timer.start()
            stdout, stderr = proc.communicate()
        finally:
            timer.cancel()
        return stdout,stderr
        
    def gpioHandler(self, state = 0):
        esp = 23
        boot = 22
        try:
            if state == 0:
                GPIO.setup(boot, GPIO.OUT)
                GPIO.output(boot, False)
                GPIO.setup(esp, GPIO.OUT)
                GPIO.output(esp, False)
                time.sleep(1)
            elif state == 1:
                GPIO.setup(boot, GPIO.OUT)
                GPIO.output(boot, True)
                time.sleep(1)
                GPIO.setup(esp, GPIO.OUT)
                GPIO.output(esp, True)
                time.sleep(1)
            elif state == 2:
                GPIO.setup(boot, GPIO.OUT)
                GPIO.output(boot, False)
                GPIO.setup(esp, GPIO.OUT)
                GPIO.output(esp, True)
                time.sleep(5)
        except:
            pass