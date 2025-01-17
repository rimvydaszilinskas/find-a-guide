"""tourguide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url, include


urlpatterns = [
    url(r'^guides/', include(('apps.guides.urls', 'guides'), namespace='guides')),
    url(r'^tours/', include(('apps.tours.urls', 'tours'), namespace='tours')),
    url(r'^users/', include(('apps.users.urls', 'users'), namespace='users')),

    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^', include(('apps.utils.urls', 'pages'), namespace='pages')),
]
