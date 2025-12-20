import math
from datetime import datetime
from app.models.donor import Donor

# Haversine formula
def distance_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(a))


def compatibility_score(donor_bg, required_bg):
    return 1.0 if donor_bg == required_bg else 0.0


def priority_score(donor: Donor, req_bg: str, lat: float, lng: float):
    dist = distance_km(lat, lng, donor.latitude, donor.longitude)
    distance_score = max(0, 1 - dist / 20)  # closer = higher score

    comp_score = compatibility_score(donor.blood_group, req_bg)

    days_old = (datetime.utcnow() - donor.created_at.replace(tzinfo=None)).days
    freshness_score = max(0, 1 - days_old / 365)

    final_score = (
        comp_score * 0.5 +
        distance_score * 0.3 +
        freshness_score * 0.2
    )

    return round(final_score, 3), round(dist, 2)
