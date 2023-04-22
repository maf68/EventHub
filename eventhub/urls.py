"""eventhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from events.views import create_event, homepage, edit_event

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("homepage/", homepage, name="homepage"),
    # path("create_event/", create_event, name="create_event"),
    # path("edit_event/", edit_event, name="edit_event"),
    path("", homepage, name="homepage"),
    path("create_event/", create_event, name="create_event"),
    path("edit_event/<int:event_id>/", edit_event, name="edit_event"),
]
