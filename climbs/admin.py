from django.contrib import admin
from .models import Mountain, Route, WeatherData

admin.site.register(Mountain)
admin.site.register(Route)
admin.site.register(WeatherData)
