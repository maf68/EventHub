from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index, name = 'Index'),
    path('Event/<int:Event_id>', views.Event_by_id, name ='Event_by_id'),
    path('Announcement/<int:Announcement_id>', views.Announcement_by_id, name ='Announcement_by_id'),
    path('EventAnnouncements/<int:Event_id>', views.get_event_announcements, name = 'Event_Announcements'),
    path('CreateAnnouncement/<int:Event_id>', views.create_announcement, name='Create_Announcement')
]