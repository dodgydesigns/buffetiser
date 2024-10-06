"""
This command can be used to test various functions in core.
"""
from django.core.management.base import BaseCommand
from core.models import Investment
from core.services.investment_details import get_all_details_for_investment, get_credit_debit_history
from core.services.update_investment import add_dividend, update_all_investment_prices

class Command(BaseCommand):
    """
    python manage.py bulk_import_reinvestments "/Users/mullsy/Downloads/reinvest.csv"
    """

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

        # update_all_investment_prices()
        # self.insert_dividends()
        self.get_all_investment_details()
        # self.get_money_in_out()


    def insert_dividends(self):
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

    def get_all_investment_details(self)
        for i in Investment.objects.all():
            dc = get_all_details_for_investment(i)
            print(dc)

    def get_money_in_out(self):
        dc = get_credit_debit_history()
        print(dc, "\n")
