from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [

    path('create_group/', views.create_group, name='create_group'),
    path('get_groups/', views.get_groups, name='get_groups'),
    path('join_group/<int:group_id>/', views.join_group, name='join_group'),
    path('send_message_to_group/<int:group_id>/', views.send_message_to_group, name='send_message_to_group'),
    path('group_messages/<int:group_id>/', views.group_messages, name='group_messages'),
    path('', TemplateView.as_view(template_name='index.html')),
  
    
    path('<str:room_name>/', views.room, name='room'),
]
