from django.core.management.base import BaseCommand
from contact.models import Contact
import csv

class Command(BaseCommand):
    help = 'Import contacts from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_path = options['csv_path']

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Contact.objects.update_or_create(
                    unique_id=row['Unique Id'],
                    defaults={
                        'contact_name': row['Contact Name'],
                        'greeting_name': row['Greeting Name']
                    }
                )

        self.stdout.write(self.style.SUCCESS('Contacts imported successfully!'))
