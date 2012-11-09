from django.db import models
from django import forms

class Msg(models.Model):
    author = models.CharField(max_length=32)
    text = models.CharField(max_length=140)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0} | {1}".format(self.author, self.text)

    class Meta:
        ordering=['-time_stamp',]

class MsgForm(forms.ModelForm):
    class Meta:
    	model=Msg
