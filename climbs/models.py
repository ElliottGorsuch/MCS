from django.db import models


class Mountain(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    elevation = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Route(models.Model):
    mountain = models.ForeignKey(Mountain, related_name='routes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    distance = models.FloatField()
    elevation_gain = models.FloatField()
    environment = models.CharField(max_length=100)
    technical_difficulty = models.CharField(max_length=100)
    glacier_travel = models.CharField(max_length=100)
    danger_factors = models.TextField()
    duration = models.FloatField()
    permit_required = models.CharField(max_length=10)
    permit_cost_over_24 = models.FloatField()
    permit_cost_under_24 = models.FloatField()
    access_difficulty = models.CharField(max_length=100)
    gear_required = models.TextField()
    final_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    difficulty_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    technical_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    danger_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    logistics_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.mountain.name}"

class WeatherData(models.Model):
    route = models.ForeignKey(Route, related_name='weather_data', on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    weather_conditions = models.TextField()
    avalanche_risk = models.CharField(max_length=20)

    def __str__(self):
        return f"Weather for {self.route.name} in {self.month}"
