from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('search/', views.EventSearchView.as_view(), name='event_search'),
    path('filter/', views.EventFilterView.as_view(), name='event_filter'),
    path('<int:id>/reviews/', views.event_reviews, name='event_reviews'),
    path('signup/', views.signup,name='signup'),
    path('login/',views.login_, name='login'),
    path('logout/',views.logout_, name='logout'),
    #path('', views.Index, name = 'Index'),
    path('announcementDetails/<int:Announcement_id>', views.Announcement_by_id, name ='announcement_by_id'),
    path('eventAnnouncements/<int:Event_id>', views.get_event_announcements, name = 'event_announcements'),
    path('createAnnouncement/<int:Event_id>', views.create_announcement, name='Create_Announcement')
]