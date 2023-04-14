"""issue_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static 

from issues.views import principal, add_watcher, delete_watcher
from users.views import profile_view, edit_profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', principal, name='principal' ),
    path('issues/', include('issues.urls')),
    #path('users/', include('users.urls')),
    path("", include("allauth.urls")),
    
    path('profile/', profile_view, name='view_profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    
    
    path('watch/<int:id>/', add_watcher, name='add_watcher'),
    path('unwatch/<int:id>/', delete_watcher, name='delete_watcher'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
