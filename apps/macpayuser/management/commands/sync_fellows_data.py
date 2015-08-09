from django.core.management.base import BaseCommand

from services.skilltree import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_new_fellows()
