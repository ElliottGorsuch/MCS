"""
URL configuration for climbing_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from climbs import views


app_name = 'climbs'

urlpatterns = [
    path('', views.mountain_list, name='mountain_list'),
    path('mountain/<int:pk>/', views.mountain_detail, name='mountain_detail'),
    path('route/<int:pk>/', views.route_detail, name='route_detail'),
]
