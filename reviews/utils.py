from django.db.models import Avg
from .models import Places, Reviews


def update_place_rating(place_id):
    reviews = Reviews.objects.filter(place_id=place_id).aggregate(
        avg_price=Avg('price'),
        avg_service=Avg('service'),
        avg_interior=Avg('interior')
    )

    avg_rating = sum(filter(None, reviews.values())) / \
        3 if any(reviews.values()) else None

    place = Places.objects.get(id=place_id)
    place.rating = avg_rating
    place.save()
