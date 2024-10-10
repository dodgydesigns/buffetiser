"""
This command takes a file containing CSV data and creates Purchases and Sales
objects from each row. Each CB (bought) and CS (sold) is of the form:
                 3       MP1         Megaport   @   283.0000    AUD
    Description: number  stock code  name           price       currency
The rows are Date, Type, Description, Name, Debit, Credit, Balance
e.g. 1/11/2022, CB, 11 VAS @ 85.4600 AUD, Vanguard Australian Shares Index ETF, 940.06, 940.06
     3/11/2023,	CS,	189 WEB @ 6.2900 AUD, Webjet, 1177.81, -1177.81
"""

import csv
from datetime import datetime

from django.core.management.base import BaseCommand

from core.models import Investment, Purchase, Sale
from core.services.update_investment import update_investment_and_history


class Command(BaseCommand):
    """
    python manage.py bulk_import_investments "/Users/mullsy/Downloads/statement.csv"
    """

    help = (
        "This function takes a file containing CSV data and creates Purchases and Sales"
        "objects from each row. Usage: "
        "python manage.py bulk_import_investments 'path_to_cmc_file'"
    )

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        # Clear the database before importing all the data.
        Investment.objects.all().delete()

        with open(options["file_path"]) as file_obj:
            reader_obj = csv.reader(file_obj)
            trade_count = 1  # CMC data only gives date so multiple trades on one day need to be distinguished
            for row in reader_obj:
                description_list = row[2].split(" ")
                if len(description_list) > 3:  # catch any blank rows
                    units, stock_code, price_per_unit = (
                        description_list[0],
                        description_list[1],
                        description_list[3],
                    )
                    investment, created = Investment.objects.get_or_create(
                        key=f"XASX-{stock_code}"
                    )
                    if created:
                        investment.symbol = stock_code
                        investment.name = row[3]
                    if row[1] == "CB":
                        purchase = Purchase(
                            investment=investment,
                            units=units,
                            price_per_unit=price_per_unit,
                            fee=11,
                            date=datetime.strptime(row[0], "%d/%m/%Y"),
                            trade_count=trade_count,
                        )
                        purchase.save()

                    elif row[1] == "CS":
                        sale = Sale(
                            investment=investment,
                            units=units,
                            price_per_unit=price_per_unit,
                            fee=11,
                            date=datetime.strptime(row[0], "%d/%m/%Y"),
                            trade_count=trade_count,
                        )
                        sale.save()
                    investment.save()
                trade_count += 1
            # Get live prices for all investments
            update_investment_and_history()