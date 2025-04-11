"""
URL configuration for chatproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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



# chatproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views
from chat import views as chat_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('signup/', account_views.signup, name='signup'),
    path('', account_views.home, name='home'),
    path('profile/', account_views.profile, name='profile'),
    path('', chat_views.home, name='home'),
    path('room/<int:room_id>/', chat_views.room, name='room'),
    path('api/get_or_create_private_room/<int:user_id>/', chat_views.get_or_create_private_room, name='get_or_create_private_room'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)