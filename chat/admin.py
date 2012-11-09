from django.contrib import admin
from models import Msg

class MsgAdmin(admin.ModelAdmin):
    pass

admin.site.register(Msg, MsgAdmin)
