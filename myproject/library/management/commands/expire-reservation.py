# myapp/management/commands/expire_reservations.py
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from library.models import Reservation


class Command(BaseCommand):
    help = 'Expires reservations older than 24 hours'

    def handle(self, *args, **kwargs):
        time_now = timezone.now() - timedelta(hours=4)
        reservations_to_delete = Reservation.objects.filter(expiry_date__lt=time_now)
        reservations_to_delete.delete()

        self.stdout.write(self.style.SUCCESS('Expired old reservations'))
