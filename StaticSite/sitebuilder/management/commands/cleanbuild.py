import os
import shutil
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.urls import reverse
from django.test.client import Client

class Command(BaseCommand):
    help = 'Clean build'

    def handle(self, *args, **option):
        if os.path.exists(settings.SITE_OUTPUT_DIRECTORY):
            shutil.rmtree(settings.SITE_OUTPUT_DIRECTORY)
    