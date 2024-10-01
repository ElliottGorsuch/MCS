# import_data.py

from django.core.management.base import BaseCommand
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from climbs.models import Mountain, Route, WeatherData

import sys
import os

# Add the path to the directory containing create_db.py
sys.path.append('/Users/jackgorsuch/Desktop/')

# Import your old SQLAlchemy models
from create_db import Mountain as OldMountain, Route as OldRoute, WeatherData as OldWeatherData

class Command(BaseCommand):
    help = 'Imports data from the old database into Django models'

    def handle(self, *args, **options):
        # Connect to the old SQLite database
        engine = create_engine('sqlite:////Users/jackgorsuch/Desktop/mountain_routes.db')
        Session = sessionmaker(bind=engine)
        session = Session()

        # Initialize a mapping dictionary to map old route IDs to new route instances
        route_mapping = {}

        # Import Mountains
        for old_mountain in session.query(OldMountain).all():
            mountain, created = Mountain.objects.get_or_create(
                name=old_mountain.name,
                defaults={
                    'location': old_mountain.location,
                    'elevation': old_mountain.elevation,
                    'latitude': old_mountain.latitude,
                    'longitude': old_mountain.longitude,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Mountain: {mountain.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Existing Mountain: {mountain.name}'))

        # Import Routes
        for old_route in session.query(OldRoute).all():
            try:
                mountain = Mountain.objects.get(name=old_route.mountain.name)
            except Mountain.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Mountain not found for route {old_route.name}'))
                continue

            route, created = Route.objects.get_or_create(
                name=old_route.name,
                mountain=mountain,
                defaults={
                    'distance': old_route.distance,
                    'elevation_gain': old_route.elevation_gain,
                    'environment': old_route.environment,
                    'technical_difficulty': old_route.technical_difficulty,
                    'glacier_travel': old_route.glacier_travel,
                    'danger_factors': old_route.danger_factors,
                    'duration': old_route.duration,
                    'permit_required': old_route.permit_required,
                    'permit_cost_over_24': old_route.permit_cost_over_24,
                    'permit_cost_under_24': old_route.permit_cost_under_24,
                    'access_difficulty': old_route.access_difficulty,
                    'gear_required': old_route.gear_required,
                }
            )

            # Map the old route ID to the new route instance
            route_mapping[old_route.id] = route

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Route: {route.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Existing Route: {route.name}'))

        # Import Weather Data
        for old_weather in session.query(OldWeatherData).all():
            route = route_mapping.get(old_weather.route_id)
            if not route:
                self.stdout.write(self.style.ERROR(f'Route not found for weather data in {old_weather.month}'))
                continue

            weather, created = WeatherData.objects.get_or_create(
                route=route,
                month=old_weather.month,
                defaults={
                    # Add any additional fields here if they exist
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created WeatherData for {route.name} in {weather.month}'))
            else:
                self.stdout.write(self.style.WARNING(f'Existing WeatherData for {route.name} in {weather.month}'))

        session.close()
