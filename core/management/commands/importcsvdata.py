import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.utils import populate_tables


class Command(BaseCommand):
    help = "Populate the database table with the data from the athlete_events.csv"

    def handle(self, *args, **options):
        csv_path = settings.ATHLETE_EVENTS_CSV_PATH

        rows = []

        with open(csv_path, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                rows.append(row)

            csvfile.close()

        populate_tables(rows)
