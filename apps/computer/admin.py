from django.contrib import admin

from apps.computer.models import Computer, ComputerImage

# Register your models here.
admin.site.register(Computer)
admin.site.register(ComputerImage)