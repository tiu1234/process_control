from django.shortcuts import render
from django.http import HttpResponse
import json

def switch_process(request):
    # if request.method == 'POST':

    return HttpResponse(json.dumps({"success": True}), content_type="application/json")

def index(request):
    return render(request, 'index.html', context={"success": 200})
