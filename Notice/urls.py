from django.urls import path
from . import views

urlpatterns = [
    path('create-notice/', views.create_notice, name='create-notice'),
    path('list/',views.notice_list, name='notice-list'),
]
