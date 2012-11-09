import models
from django.shortcuts import render

class Chat(object):
    def __init__(self):
        pass

    def index(self, request):
        form = models.MsgForm()
        msg_list = models.Msg.objects.all()
        return render(request, 'index.html', {
            'form': form,
            'msg_list': msg_list,
        })

    def send(self, request):
        pass

    def update(self, request):
        pass

chat = Chat()
index = chat.index
send = chat.send
update = chat.update