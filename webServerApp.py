from time import time,sleep
import json
from typing import IO
from flask import Flask, jsonify, render_template, request
from flask.wrappers import Request
import esp
import os
from sys import getsizeof
from gitCLI import Git

STATIC_PATH = 'main'
STATIC_URL_PATH = '/main'
TEMPLATE_PATH = 'main/template/'

app = Flask(__name__,template_folder=TEMPLATE_PATH,static_url_path=STATIC_URL_PATH,static_folder=STATIC_PATH)

esp = esp.Esp()

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/overview')
def overview():
    return render_template('overview.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/updateData')
def updateData():
    datalayer = {'Status':esp.status}
    response = app.response_class(
        response =json.dumps(datalayer),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/test',methods = ['POST','GET'])
def test():
    for i in request.form:
        data = json.loads(i)
        if data["cmd"] == "start_flashing":
            esp.start_flash()
            datalayer = {'Status':esp.status}
        elif data["cmd"] == "get_firmware_version":
            datalayer = {'Status':esp.firmwareVersion}
        elif data["cmd"] == "start_test":
            test_report = esp.start_testing()
            datalayer = {'Status':esp.status,"Report":test_report}

    response = app.response_class(
        response =json.dumps(datalayer),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ =='__main__':
    try:
        print("Try to udpate git repository")
        git_repo = Git()
        git_repo.pull()
        print("Update was succesfull!")
    except Exception as e:
        print("Error during git pull reqiest: ",e)
    app.run(host="0.0.0.0",port=8000,debug=True)
    #loop = asyncio.get_event_loop

