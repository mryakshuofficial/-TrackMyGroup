"""
URL configuration for TrackMyGroup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from core import views
from Notice import urls 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Notice.urls')),
    path('', views.home),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('dashboard/', views.dashboard),

    path('create-group/', views.create_group, name='create-group'),
    path('join-group/', views.join_group, name='join-group'),
    path('group-map/<int:group_id>/', views.group_map, name='group-map'),
    path('group/<int:group_id>/locations/', views.group_locations_api, name="group_locations_api"),
    path('group/<int:group_id>/update-location/', views.update_location, name="update_location"),
    
]
