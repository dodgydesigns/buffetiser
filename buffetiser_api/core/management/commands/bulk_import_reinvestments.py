"""
This command takes a file containing CSV data and creates DividendReinvestment 
object from each row. Each row is of the form:
                 VDHG,          16/07/2024  3
    Description: stock code     Date        Units
e.g. VDHG,16/07/2024,3
"""
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from core.models import DividendReinvestment, Investment
from core.services.update_investment import add_dividend, get_all_details_for_investment, get_units_held_at_date, update_all_investment_prices

class Command(BaseCommand):
    """
    python manage.py bulk_import_reinvestments "/Users/mullsy/Downloads/reinvest.csv"
    """
    help = "This function takes a file containing CSV data and creates DividendReinvestment" \
        "and DividendPayment objects from each row. Usage: " \
        "python manage.py bulk_import_dividends 'path_to_cmc_file'"
 
    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):


        for i in Investment.objects.all():
            dc = get_all_details_for_investment(i)

        update_all_investment_prices()
        inv = Investment.objects.filter(symbol="VAS").first()
        add_dividend(inv,
                 True,
                 "01/10/2024",
                 "16/10/2024",
                 103.32)
        inv = Investment.objects.filter(symbol="VDHG").first()
        add_dividend(inv,
                 True,
                 "01/10/2024",
                 "16/10/2024",
                 36.97)
        inv = Investment.objects.filter(symbol="VGS").first()
        add_dividend(inv,
                 True,
                 "01/10/2024",
                 "16/10/2024",
                 28.81)
        inv = Investment.objects.filter(symbol="VTS").first()
        add_dividend(inv,
                 True,
                 "27/09/2024",
                 "24/10/2024",
                 107.57)


        with open(options["file_path"]) as file_obj:
            reader_obj = csv.reader(file_obj)
            for row in reader_obj:
                investment = Investment.objects.filter(symbol=row[0]).first()
                date_elements = row[1].split("/")
                reinvestment_date = datetime(int(date_elements[2]),
                                             int(date_elements[1]), 
                                             int(date_elements[0]))
                # cutoff_date isn't correct but it's too much work to figure out the real cutoff date
                # as it's not provided in 'statements'. Creating a DividendReinvestment object
                # when it shows up will be easy as the details are available when it happens.
                reinvest = DividendReinvestment(
                    investment=investment,
                    cutoff_date=reinvestment_date,
                    reinvestment_date=reinvestment_date,
                    units=int(row[2])
                )
                reinvest.save()
