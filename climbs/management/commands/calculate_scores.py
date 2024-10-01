from django.core.management.base import BaseCommand
from climbs.models import Route
from climbs import scoring
from decimal import Decimal

class Command(BaseCommand):
    help = 'Calculates and updates the scores for all routes'

    def handle(self, *args, **options):
        # Fetch all routes
        all_routes = Route.objects.select_related('mountain').all()

        # Lists to store raw scores
        difficulty_scores = []
        technical_scores = []
        danger_scores = []
        logistics_scores = []

        # Dictionaries to map route id to raw scores
        route_difficulty_scores = {}
        route_technical_scores = {}
        route_danger_scores = {}
        route_logistics_scores = {}

        # First, calculate the raw scores for each route
        for route in all_routes:
            # Get the attributes needed for scoring
            distance = route.distance or 0
            elevation_gain = route.elevation_gain or 0
            mountain_elevation = route.mountain.elevation or 0
            technical_difficulty = route.technical_difficulty or ''
            glacier_travel = 'Yes' if route.glacier_travel else 'No'
            oxygen = 'Oxygen' in (route.gear_required or '')
            danger_factors = route.danger_factors or ''
            latitude = route.mountain.latitude or 0
            avalanche_risk = 'Unknown'
            temperature = 0
            elevation = mountain_elevation
            permit_required = route.permit_required
            duration = route.duration or 0
            gear_required = route.gear_required or ''
            permit_cost = route.permit_cost_over_24 or 0
            access_difficulty = route.access_difficulty or ''
            environment = route.environment or ''

            # Calculate raw scores
            raw_difficulty_score = scoring.score_difficulty(distance, elevation_gain, mountain_elevation)
            raw_technical_score = scoring.score_technical(technical_difficulty, glacier_travel, oxygen)
            raw_danger_score = scoring.score_danger(
                danger_factors,
                latitude,
                avalanche_risk,
                temperature,
                technical_difficulty,
                elevation
            )
            raw_logistics_score = scoring.score_logistics(
                permit_required,
                duration,
                gear_required,
                permit_cost,
                access_difficulty,
                environment
            )['Total Logistics Score']

            # Store the raw scores
            route_difficulty_scores[route.id] = raw_difficulty_score
            route_technical_scores[route.id] = raw_technical_score
            route_danger_scores[route.id] = raw_danger_score
            route_logistics_scores[route.id] = raw_logistics_score

            # Append to the lists
            difficulty_scores.append(raw_difficulty_score)
            technical_scores.append(raw_technical_score)
            danger_scores.append(raw_danger_score)
            logistics_scores.append(raw_logistics_score)

        # Calculate min and max scores for normalization
        min_difficulty = min(difficulty_scores) if difficulty_scores else 0
        max_difficulty = max(difficulty_scores) if difficulty_scores else 100
        min_technical = min(technical_scores) if technical_scores else 0
        max_technical = max(technical_scores) if technical_scores else 100
        min_danger = min(danger_scores) if danger_scores else 0
        max_danger = max(danger_scores) if danger_scores else 100
        min_logistics = min(logistics_scores) if logistics_scores else 0
        max_logistics = max(logistics_scores) if logistics_scores else 100

        # Now, calculate normalized scores and update routes
        for route in all_routes:
            # Get raw scores
            raw_difficulty_score = route_difficulty_scores.get(route.id, 0)
            raw_technical_score = route_technical_scores.get(route.id, 0)
            raw_danger_score = route_danger_scores.get(route.id, 0)
            raw_logistics_score = route_logistics_scores.get(route.id, 0)

            # Normalize scores
            normalized_difficulty_score = scoring.normalize_score(raw_difficulty_score, min_difficulty, max_difficulty)
            normalized_technical_score = scoring.normalize_score(raw_technical_score, min_technical, max_technical)
            normalized_danger_score = scoring.normalize_score(raw_danger_score, min_danger, max_danger)
            normalized_logistics_score = scoring.normalize_score(raw_logistics_score, min_logistics, max_logistics)

            # Calculate final score
            final_score = (
                normalized_difficulty_score * 0.3 +
                normalized_technical_score * 0.3 +
                normalized_danger_score * 0.2 +
                normalized_logistics_score * 0.2
            )
            final_score = min(final_score, 100)
            final_score = round(final_score, 2)

            # Update route
            route.final_score = Decimal(final_score)
            route.difficulty_score = Decimal(round(normalized_difficulty_score, 2))
            route.technical_score = Decimal(round(normalized_technical_score, 2))
            route.danger_score = Decimal(round(normalized_danger_score, 2))
            route.logistics_score = Decimal(round(normalized_logistics_score, 2))
            route.save()

            self.stdout.write(f"Updated {route.name}: Final Score {route.final_score}")

        self.stdout.write(self.style.SUCCESS('Successfully updated scores for all routes.'))

