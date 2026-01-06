from django.urls import path
from . import views, auth_views

app_name = 'custom_admin'

urlpatterns = [
    # Dashboard
    path('', views.admin_dashboard, name='dashboard'),
    
    # Gestion des utilisateurs
    path('users/', views.admin_users_list, name='users_list'),
    path('users/create/', views.admin_user_create, name='user_create'),
    path('users/<int:user_id>/update/', views.admin_user_update, name='user_update'),
    path('users/<int:user_id>/delete/', views.admin_user_delete, name='user_delete'),
    
    # Gestion des réunions
    path('meetings/', views.admin_meetings_manage, name='meetings_manage'),
    
    # Gestion des participants
    path('participants/', views.admin_participants_manage, name='participants_manage'),
]
