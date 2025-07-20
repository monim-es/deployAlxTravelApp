from django.core.management.base import BaseCommand
from listings.models import Listing
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        sample_data = [
            {"title": "Cozy Cabin", "description": "A small cabin in the woods", "price_per_night": 100.00, "location": "Colorado"},
            {"title": "Beach House", "description": "A house on the beach", "price_per_night": 250.00, "location": "Malibu"},
        ]

        for data in sample_data:
            Listing.objects.create(**data)

        self.stdout.write(self.style.SUCCESS("Sample listings created."))
