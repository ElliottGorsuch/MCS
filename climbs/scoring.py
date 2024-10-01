import re
import math
from difflib import get_close_matches
from decimal import Decimal
from .models import Mountain, Route


# Define scoring functions
def score_difficulty(distance, elevation_gain, mountain_elevation):
    distance_weight = 0.25
    gain_weight = 0.37
    elevation_weight = 0.38

    distance_score = distance * distance_weight
    gain_score = elevation_gain * gain_weight
    elevation_score = mountain_elevation * elevation_weight

    difficulty_score = distance_score + gain_score + elevation_score
    return difficulty_score

def parse_technical_grade(technical_difficulty):
    class_grade = None
    rock_grade = None
    ice_grade = None
    aid_grade = None

    grades = re.split(r',\s*', technical_difficulty)

    for grade in grades:
        grade = grade.strip()

        if re.match(r'Class \d+(\.\d+)?', grade):
            if 'Class 5.' in grade:
                class_grade = 'Class 5'
                rock_grade = re.search(r'5\.\d+', grade).group()
            else:
                class_grade = grade
        elif re.match(r'5\.\d+', grade):
            rock_grade = grade
            if class_grade is None:
                class_grade = 'Class 5'
        elif re.match(r'WI-\d+', grade):
            ice_grade = grade
        elif re.match(r'[AC]\d+', grade):
            aid_grade = grade

    return class_grade, rock_grade, ice_grade, aid_grade

def score_technical(technical_difficulty, glacier_travel, oxygen):
    rock_grades = {
        'Class 1': 0,
        'Class 2': 10,
        'Class 3': 20,
        'Class 4': 50,
        'Class 5': 100,
        '5.0': 110,
        '5.5': 120,
        '5.6': 130,
        '5.7': 140,
        '5.8': 150,
        '5.9': 160,
        '5.10': 170,
        '5.11': 180,
        '5.12': 190,
        '5.13': 200,
        '5.14': 220,
    }

    ice_grades = {
        'WI-1': 10,
        'WI-2': 30,
        'WI-3': 50,
        'WI-4': 70,
        'WI-5': 90,
    }

    aid_grades = {
        'A1': 20,
        'A2': 50,
        'A3': 80,
        'A4': 100,
        'C1': 20,
        'C2': 50,
        'C3': 80,
        'C4': 100,
    }

    class_grade, rock_grade, ice_grade, aid_grade = parse_technical_grade(technical_difficulty)

    tech_score = 0

    if class_grade:
        tech_score += rock_grades.get(class_grade, 0)
    if rock_grade:
        tech_score += rock_grades.get(rock_grade, 0)
    if ice_grade:
        tech_score += ice_grades.get(ice_grade, 0)
    if aid_grade:
        tech_score += aid_grades.get(aid_grade, 0)

    glacier_scores = {
        'No': 0,
        'Yes but No Crevasses': 20,
        'Yes and Crevasses': 30,
        'Yes Crevasses and More Than 50% of Route': 40,
    }
    glacier_score = glacier_scores.get(glacier_travel, 0)

    oxygen_score = 10 if oxygen else 0

    total_score = tech_score + glacier_score + oxygen_score

    return total_score

def score_danger(danger_factors, latitude, avalanche_risk, temperature, technical_difficulty, elevation):
    danger_scores = {
        'Technical aid climbing': 20,
        'Thunderstorms': 10,
        'High winds': 10,
        'Altitude sickness': 15,
        'Steep ice climbing': 20,
        'Long duration': 10,
        'Steep terrain': 15,
        'Vertical terrain': 20,
        'Exposure': 15,
        'Minimal exposure': 5,
        'Remote location': 15,
        'Afternoon thunderstorms': 10,
        'Rockfall': 15,
        'Snow/ice conditions': 15,
        'Avalanches': 20,
        'Icefall': 20,
        'Rugged terrain': 15,
        'Volcanic activity': 20,
        'Extreme cold': 20,
        'Weather': 10,
        'Loose rock': 15,
        'Oxygen depletion': 20,
        'Crevasses': 20,
        'Loose scree': 10,
        'Glacier travel': 20,
        'Scrambling': 10,
        'Route-finding': 10,
        'Snow travel': 15,
    }

    factors = [factor.strip() for factor in danger_factors.split(',') if factor.strip()]
    factor_scores = [danger_scores.get(factor, 0) for factor in factors]
    if not factor_scores:
        danger_factors_score = 0
    else:
        average_factor_score = sum(factor_scores) / len(factor_scores)
        danger_factors_score = average_factor_score

    avalanche_risk_map = {
        'Low': 5,
        'Moderate': 10,
        'Considerable': 15,
        'High': 20,
        'Extreme': 25,
        'Unknown': 0
    }

    def get_avalanche_risk(risk_description):
        risk_description = risk_description.lower().strip()
        possible_risks = list(avalanche_risk_map.keys())
        match = get_close_matches(risk_description.capitalize(), possible_risks, n=1, cutoff=0.6)
        return match[0] if match else 'Unknown'

    risk_category = get_avalanche_risk(avalanche_risk)
    avalanche_risk_score = avalanche_risk_map.get(risk_category, 0)

    def temperature_to_danger_score(temperature):
        if temperature <= -40:
            return 25
        elif temperature <= -30:
            return 20
        elif temperature <= -20:
            return 15
        elif temperature <= -10:
            return 10
        elif temperature <= 0:
            return 5
        else:
            return 0

    temperature_danger_score = temperature_to_danger_score(temperature)

    def latitude_to_danger_score(latitude):
        abs_latitude = abs(latitude)
        if abs_latitude >= 70:
            return 20
        elif abs_latitude >= 60:
            return 15
        elif abs_latitude >= 50:
            return 10
        elif abs_latitude >= 40:
            return 5
        else:
            return 0

    latitude_danger_score = latitude_to_danger_score(latitude)

    def technical_difficulty_to_danger_score(technical_difficulty):
        if 'Class 5' in technical_difficulty or '5.' in technical_difficulty:
            return 40
        elif 'Class 4' in technical_difficulty:
            return 30
        elif 'Class 3' in technical_difficulty:
            return 20
        else:
            return 10

    technical_difficulty_danger_score = technical_difficulty_to_danger_score(technical_difficulty)

    def altitude_to_danger_score(elevation):
        if elevation >= 8000:
            return 50
        elif elevation >= 7000:
            return 40
        elif elevation >= 6000:
            return 30
        elif elevation >= 5000:
            return 20
        elif elevation >= 4000:
            return 10
        else:
            return 5

    altitude_danger_score = altitude_to_danger_score(elevation)

    total_danger_score = (
        danger_factors_score * 0.1 +
        avalanche_risk_score * 0.1 +
        temperature_danger_score * 0.1 +
        latitude_danger_score * 0.1 +
        technical_difficulty_danger_score * 0.3 +
        altitude_danger_score * 0.3
    )

    max_possible_score = 60
    total_danger_score = (total_danger_score / max_possible_score) * 100
    total_danger_score = min(total_danger_score, 100)

    if len(factors) == 0:
        total_danger_score *= 0.9
    elif len(factors) >= 5:
        total_danger_score *= 1.05
        total_danger_score = min(total_danger_score, 100)

    total_danger_score = round(total_danger_score, 2)

    return total_danger_score

def score_logistics(permit_required, duration, gear_required, permit_cost, access_difficulty, environment=None):
    permit_score = min(permit_cost / 100, 50)
    duration_score = min(duration * 10, 50)

    gear_weights = {
        'ice axe': 15, 'crampons': 15, 'rope': 10, 'helmet': 5, 'harness': 10,
        'belay device': 5, 'protection gear': 20, 'trad rack': 50,
        'portaledge': 25, 'technical boots': 10, 'fixed rope': 20, 'tent': 10,
        'sleeping bag': 5, 'carabiners': 5, 'gloves': 3, 'goggles': 3, 'shovel': 8,
        'beacon': 10, 'avalanche probe': 8
    }

    gear_items = [item.strip() for item in re.split(r',\s*', gear_required) if item.strip()]
    total_gear_difficulty = sum(gear_weights.get(item.lower(), 0) for item in gear_items)

    if duration > 2:
        total_gear_difficulty *= (1 + (duration / 10))

    if 'trad rack' in gear_items and 'remote' in access_difficulty.lower():
        total_gear_difficulty *= 1.3

    total_gear_difficulty = min(total_gear_difficulty, 100)

    remoteness_mapping = {
        'easy': 10, 'moderate': 20, 'difficult': 30, 'very difficult': 40,
        'extremely difficult': 50, 'remote': 40, 'very remote': 50, 'extremely remote': 60
    }

    match = re.search(r'(easy|moderate|difficult|very difficult|extremely difficult|remote|very remote|extremely remote)', access_difficulty.lower())
    if match:
        general_level = match.group(1)
        remoteness_score = remoteness_mapping.get(general_level, 0)
    else:
        remoteness_score = 0

    if environment and 'glacier' in environment.lower():
        remoteness_score += 10

    weights = {
        'permit': 0.25, 'duration': 0.25, 'gear': 0.25, 'remoteness': 0.25
    }

    total_logistics_score = (
        permit_score * weights['permit'] +
        duration_score * weights['duration'] +
        total_gear_difficulty * weights['gear'] +
        remoteness_score * weights['remoteness']
    )
    total_logistics_score = min(total_logistics_score, 100)

    return {
        'Total Logistics Score': round(total_logistics_score, 2),
    }

def normalize_score(score, min_score, max_score):
    if max_score == min_score:
        return 50
    return (score - min_score) / (max_score - min_score) * 99 + 1
