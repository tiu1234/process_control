from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

import subprocess
import os, signal
import time

from psutil import process_iter
from signal import SIGTERM

@csrf_exempt
def switch_process(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['action'] == "remote_control":
            os.environ.setdefault('DJANGO_SETTINGS_MODULE','remote_control.settings')
            subprocess.call(['python3', '/home/pi/final/SunFounder_PiCar-V/remote_control/manage.py', 'runserver'])
            subprocess.call(['/home/pi/ngrok', 'http', '8000', "-subdomain=remote-control"])
        elif data['action'] == "deep_pi_car":
            for proc in process_iter():
                for conns in proc.connections(kind='inet'):
                    if conns.laddr.port == 8000:
                        proc.send_signal(SIGTERM)
            subprocess.call(['python3', '/home/pi/DeepPiCar/driver/code/deep_pi_car.py'])

        return HttpResponse(json.dumps({"success": True, "action": data['action']}), content_type="application/json")

    return HttpResponse(json.dumps({"success": True}), content_type="application/json")

def index(request):
    return render(request, 'index.html', context={"success": 200})
