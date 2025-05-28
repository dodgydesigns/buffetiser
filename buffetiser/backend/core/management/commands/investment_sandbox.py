"""
This command can be used to test various functions in core.
"""

import json

from django.core.management.base import BaseCommand

from core.models import Investment
from core.services.investment_details import (
    get_all_details_for_investment, scraper_function_get_daily_change,
    scraper_function_investment_and_history)
from core.services.investment_helpers import initiate_async_scrape


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