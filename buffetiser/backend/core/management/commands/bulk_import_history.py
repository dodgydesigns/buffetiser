"""
This function takes a file containing CSV data and creates Investment History
objects from each row.
                 MP1     7/4/2025   OPEN   HIGH   LOW   CLOSE
    Description: Symbol  date       price   price  price  price
e.g.             ABC    7/4/2025   1.00   1.10   0.90   1.05
"""

import csv
from datetime import datetime

from core.models import History, Investment, Purchase, Sale
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    python manage.py bulk_import_investments "/Users/mullsy/Downloads/statement.csv"
    """

    help = (
        "This function takes a file containing CSV data and creates Investment History"
        "objects from each row. Usage: "
        "python manage.py bulk_import_history 'path_to_file'"
    )

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        with open(options["file_path"]) as file_obj:
            reader_obj = csv.reader(file_obj)
            for row in reader_obj:
                investment = Investment.objects.filter(symbol=row[0]).first()
                if investment:
                    history_obj = History(
                        investment=investment,
                        date=datetime.strptime(row[1], "%d/%m/%Y"),
                        high=float(row[2]),
                        low=float(row[3]),
                        close=float(row[4]),
                    )
                    history_obj.save()