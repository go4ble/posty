import models
from django.shortcuts import render
import json
from django.http import HttpResponse
from django.core import serializers
from gevent.event import Event
from datetime import datetime

class Chat(object):
    def __init__(self):
        # at some point, may want to implement a buffer for messages
        # self.buffer = []
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
            form = models.MsgForm(request.POST)
            if form.is_valid():
                form.save()
                # tell everyone who's waiting on msg_event that a msg was just
                # posted
                self.msg_event.set()
                self.msg_event.clear()
                return HttpResponse(json.dumps(True), mimetype='application/json')
        return HttpResponse(json.dumps(False), mimetype='application/json')

    def update(self, request):
        check_time = datetime.now()
        # wait for next msg post
        self.msg_event.wait()
        msg_list = models.Msg.objects.filter(time_stamp__gte=check_time)
        return HttpResponse(serializers.serialize('xml', msg_list), mimetype='text/xml')

chat = Chat()
index = chat.index
send = chat.send
update = chat.update