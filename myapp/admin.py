from django.contrib import admin
from .models import Program, Comment, Station

admin.site.register(Program)
admin.site.register(Comment)
admin.site.register(Station)