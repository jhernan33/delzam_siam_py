"""siam URL Configuration

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
from django import views
# from django.urls import path
from django.conf.urls import include
from rest_framework.authtoken import views

from django.urls import include, path
# from debug_toolbar.toolbar import debug_toolbar_urls
# import debug_toolbar

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('' , include('asiam.urls')),
    path('api_generate_token/', views.obtain_auth_token),
    # path('__debug__/', include(debug_toolbar.urls)),
    # path('siam/o/',include('oauth2_provider.urls', namespace='oauth2_provider')),

] # + debug_toolbar_urls()
