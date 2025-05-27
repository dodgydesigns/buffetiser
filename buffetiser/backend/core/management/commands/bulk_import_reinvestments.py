"""
This command takes a file containing CSV data and creates DividendReinvestment
object from each row. Each row is of the form:
                 VDHG,          16/07/2024  3
    Description: stock code     Date        Units
e.g. VDHG,16/07/2024,3
"""

import csv
from datetime import datetime

from core.models import DividendReinvestment, Investment
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    python manage.py bulk_import_reinvestments "/Users/mullsy/Downloads/reinvest.csv"
    """

    help = (
        "This function takes a file containing CSV data and creates DividendReinvestment"
        "and DividendPayment objects from each row. Usage: "
        "python manage.py bulk_import_dividends 'path_to_cmc_file'"
    )

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        with open(options["file_path"]) as file_obj:
            reader_obj = csv.reader(file_obj)
            for row in reader_obj:
                investment = Investment.objects.filter(symbol=row[0]).first()
                date_elements = row[1].split("/")
                date = datetime(int(date_elements[2]), int(date_elements[1]), int(date_elements[0]))
                # cutoff_date isn't correct but it's too much work to figure out the real cutoff date
                # as it's not provided in 'statements'. Creating a DividendReinvestment object
                # when it shows up will be easy as the details are available when it happens.
                reinvest = DividendReinvestment(
                    investment=investment,
                    cutoff_date=date,
                    date=date,
                    units=int(row[2]),
                )
                reinvest.save()
