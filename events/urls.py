from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('search/', views.EventSearchView.as_view(), name='event_search'),
    path('filter/', views.EventFilterView.as_view(), name='event_filter'),
    path('signup/', views.signup,name='signup'),
    path('login/',views.login_, name='login'),
    path('logout/',views.logout_, name='logout'),
    path("create_event/", views.create_event, name="create_event"),
    path("edit_event/<int:event_id>/", views.edit_event, name="edit_event"),
]