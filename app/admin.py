from django.contrib import admin
from .models import Event
from .models import MyUser
from .models import Announcement
# Register your models here.
admin.site.register(Event)
admin.site.register(MyUser)
admin.site.register(Announcement)