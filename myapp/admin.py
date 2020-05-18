from django.contrib import admin
from .models import *


class StationInline(admin.StackedInline):
    model = Station
    extra = 3

class DjInline(admin.StackedInline):
    model = Dj
    extra = 3

class ListenerInline(admin.StackedInline):
    model = Listener
    extra = 3

class ProgramAdmin(admin.ModelAdmin):
    inlines = [DjInline, StationInline, ListenerInline]


admin.site.register(Program, ProgramAdmin)
# 一応、ファイル単体の管理画面も作っておく
admin.site.register(Station) 
admin.site.register(Comment) 
admin.site.register(Week) 
admin.site.register(Genre) 
admin.site.register(Dj) 
admin.site.register(Listener) 
admin.site.register(Okini) 
admin.site.register(Info) 