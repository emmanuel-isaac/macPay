from django.core.management.base import BaseCommand
import webbrowser



from services.skilltree import *


class Command(BaseCommand):

	def handle(self, *args, **options):
		sync_new_fellows()
		