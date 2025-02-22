"""
This command can be used to test various functions in core.
"""

import json

from core.models import Investment
from core.services.investment_details import (
    get_all_details_for_investment, get_credit_debit_history,
    scraper_function_get_daily_change, scraper_function_investment_and_history)
from core.services.investment_helpers import initiate_async_scrape
from core.services.investment_updaters import add_dividend
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    python manage.py investment_sandbox "/Users/mullsy/Downloads/reinvest.csv"
    """

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        initiate_async_scrape(scraper_function_investment_and_history)
        initiate_async_scrape(scraper_function_get_daily_change)

        self.get_all_investment_details()
        # self.get_money_in_out()

    def get_all_investment_details(self):
        all = []
        for inv in list(Investment.objects.all()):
            all.append(get_all_details_for_investment(inv))
        # print(json.dumps(all))

    # def insert_dividends(self):
    #     inv = Investment.objects.filter(symbol="VAS").first()
    #     add_dividend(inv, True, "01/10/2024", "16/10/2024", 103.32)
    #     inv = Investment.objects.filter(symbol="VDHG").first()
    #     add_dividend(inv, True, "01/10/2024", "16/10/2024", 36.97)
    #     inv = Investment.objects.filter(symbol="VGS").first()
    #     add_dividend(inv, True, "01/10/2024", "16/10/2024", 28.81)
    #     inv = Investment.objects.filter(symbol="VTS").first()
    #     add_dividend(inv, True, "27/09/2024", "24/10/2024", 107.57)

    # def get_money_in_out(self):
    #     dc = get_credit_debit_history()
    #     print(dc, "\n")
