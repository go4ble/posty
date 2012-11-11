import models
from django.shortcuts import render
import json, time
from django.http import HttpResponse
from django.core import serializers
from gevent.event import Event
from datetime import datetime

class Chat(object):
    def __init__(self):
        self.buffer = []
        self.msg_event = Event()

    def index(self, request):
        form = models.MsgForm()
        msg_list = models.Msg.objects.all()
        return render(request, 'index.html', {
            'form': form,
            'msg_list': msg_list,
        })

    def send(self, request):
        if request.method == 'POST':
            time.sleep(2)
            form = models.MsgForm(request.POST)
            if form.is_valid():
                form.save()
                self.msg_event.set()
                self.msg_event.clear()
                return HttpResponse(json.dumps(True), mimetype='application/json')
        return HttpResponse(json.dumps(False), mimetype='application/json')

    def update(self, request):
        check_time = datetime.now()
        self.msg_event.wait()
        msg_list = models.Msg.objects.filter(time_stamp__gte=check_time)
        #return HttpResponse(write_json(msg_list), mimetype='application/json')
        return HttpResponse(serializers.serialize('xml', msg_list), mimetype='text/xml')

chat = Chat()
index = chat.index
send = chat.send
update = chat.update

'''
def write_json(msg_list):
    value = '"msg_list": ['
    for i in range(0, len(msg_list)):
        msg = msg_list[i]
        value += '{"author": "' + msg.author
        value += '", "text": "' + msg.text
        value += '", "time_stamp": "' + msg.time_stamp.__str__()
        value += '"}'
        if i != len(msg_list) - 1:
            value += ','
    value += ']'
    return value
'''