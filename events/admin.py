from django.contrib import admin
from .models import Event, MyUser, Review, Announcement

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'location')
    search_fields = ('title', 'location')
    list_filter = ('city',)

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'nationality', 'is_promoter')
    search_fields = ('first_name', 'last_name', 'username', 'email')
    list_filter = ('is_promoter', 'nationality')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'comment', 'rating', 'created_at')
    list_filter = ('event', 'created_at')
    search_fields = ('event__title', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
#list_display attribute that specifies the fields to be 
#displayed in the admin interface, a search_fields 
#attribute that specifies fields to be searched on, 
#and a list_filter attribute that specifies filters to be used.

admin.site.register(Event, EventAdmin)
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Announcement)