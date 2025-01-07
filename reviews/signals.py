from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from reviews.models import Reviews
from .utils import update_place_rating


@receiver(post_save, sender=Reviews)
@receiver(post_delete, sender=Reviews)
def recalculate_rating(sender, instance, **kwargs):
    update_place_rating(instance.place_id.id)
