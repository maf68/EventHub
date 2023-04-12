from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('search/', views.EventSearchView.as_view(), name='event_search'),
    path('filter/', views.EventFilterView.as_view(), name='event_filter'),
]