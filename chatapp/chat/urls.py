from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    # path('start/', views.start_convo, name='start_convo'),
    # path('<int:convo_id>/', views.get_conversation, name='get_conversation'),
    # path('', views.conversations, name='conversations'),
    path('<str:room_name>/', views.room, name='room'),
    path('', TemplateView.as_view(template_name='index.html')),
]
