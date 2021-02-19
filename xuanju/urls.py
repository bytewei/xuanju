"""xuanju URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from navi.views import NaviView

urlpatterns = [
    path('admin/', admin.site.urls),
    # index for temp
    path('', NaviView.as_view(), name='index'),

    # navi
    path('navi/', include(('navi.urls', 'navi'), namespace='navi')),

    # users
    path('users/', include(('users.urls', 'users'), namespace='users')),

    # captcha
    path('captcha/', include('captcha.urls')),
]
