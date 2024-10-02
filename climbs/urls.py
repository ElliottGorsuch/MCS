
from django.urls import path
from . import views

app_name = 'climbs'

urlpatterns = [
    path('', views.mountain_list, name='mountain_list'),
    path('mountain/<int:pk>/', views.mountain_detail, name='mountain_detail'),
    path('route/<int:pk>/', views.route_detail, name='route_detail'),
    # Add other URL patterns as needed
]

