from django.contrib import admin
from .models import Event, MyUser

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'location')
    search_fields = ('title', 'location')
    list_filter = ('city',)

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'nationality', 'is_promoter')
    search_fields = ('first_name', 'last_name', 'username', 'email')
    list_filter = ('is_promoter', 'nationality')

admin.site.register(Event, EventAdmin)
admin.site.register(MyUser, MyUserAdmin)