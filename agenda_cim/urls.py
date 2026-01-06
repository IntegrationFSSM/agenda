"""
URL configuration for agenda_cim project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from custom_admin import auth_views, password_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redirect homepage to login
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    
    # Authentication
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('profile/', auth_views.profile_view, name='profile'),
    path('change-password/', password_views.change_password_first_login, name='change_password_first_login'),
    
    # Custom Admin
    path('custom-admin/', include('custom_admin.urls', namespace='custom_admin')),
    
    # Meetings app
    path('', include('meetings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
