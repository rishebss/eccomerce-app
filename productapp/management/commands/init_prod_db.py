from django.core.management.base import BaseCommand
from django.conf import settings
import os
import subprocess
import json


class Command(BaseCommand):
    help = "Initialize production database with Turso data"

    def handle(self, *args, **options):
        self.stdout.write("Initializing production database...")

        # Ensure /tmp directory exists
        os.makedirs("/tmp", exist_ok=True)

        try:
            # Run sync from Turso to populate production DB
            result = subprocess.run(
                ["python", "manage.py", "sync_turso"], capture_output=True, text=True
            )

            if result.returncode == 0:
                self.stdout.write(
                    self.style.SUCCESS("Production database initialized successfully!")
                )
            else:
                self.stdout.write(self.style.ERROR(f"Failed to sync: {result.stderr}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Initialization failed: {str(e)}"))
