from django.urls import path
from . import views

urlpatterns = [
    # Calendrier
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/meetings/', views.meeting_list_json, name='meeting_list_json'),
    
    # Réunions
    path('meeting/<int:pk>/', views.meeting_detail, name='meeting_detail'),
    path('meeting/create/', views.meeting_create, name='meeting_create'),
    path('meeting/<int:pk>/update/', views.meeting_update, name='meeting_update'),
    path('meeting/<int:pk>/delete/', views.meeting_delete, name='meeting_delete'),
]
