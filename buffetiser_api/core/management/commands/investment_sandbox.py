"""
This command can be used to test various functions in core.
"""
import asyncio
import aiohttp
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup

from core.models import Investment
from core.services.investment_details import (get_all_details_for_investment,
                                              get_credit_debit_history, get_details_for_all_investments)
from core.services.update_investment import (add_dividend,
                                             get_live_price)


class Command(BaseCommand):
    """
    python manage.py investment_sandbox "/Users/mullsy/Downloads/reinvest.csv"
    """

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        # for inv in list(Investment.objects.all()):
            # get_live_price(inv)
        # self.insert_dividends()
        # self.get_all_investment_details()
        # self.get_money_in_out()
        self.get_all_stuff()

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

    def get_all_investment_details(self):
        for i in Investment.objects.all():
            dc = get_details_for_all_investments()
            print(dc)

    def get_money_in_out(self):
        dc = get_credit_debit_history()
        print(dc, "\n")


    # @sync_to_async
    # def get_investments(self):
    #     return 

    @sync_to_async
    def get_investment_and_urls(self):
        """
        Get each Investment and the URL containing the data for that investment. This information can then
        be used to scrape the page and get the values needed.
        """
        investment_and_url = {}
        for investment in list(Investment.objects.all()):
            investment_and_url[investment.symbol] = {"investment": investment,
                                                     "url": f"https://bigcharts.marketwatch.com/quotes/multi.asp?view=q&msymb=au:{investment.symbol}+"}
        return investment_and_url

    async def fetch(self, session, url):
        """
        Get all the data from the page.
        """
        async with session.get(url) as response:
            return await response.text()

    async def scrape(self):
        """
        Scrape the source for each Investment. Update the the live price for each and create an entry
        into the investment's value history.
        """
        investment_and_url = await self.get_investment_and_urls()
        async with aiohttp.ClientSession() as session:
            tasks = []
            for value in investment_and_url.values():
                page_data = self.fetch(session, value["url"])
                tasks.append(asyncio.ensure_future(page_data))
            responses = await asyncio.gather(*tasks)

            for response in responses:
                soup = BeautifulSoup(response, "html.parser")
                symbol = soup.find("td", {"class": "symb-col"}).text
                last_price = soup.find("td", {"class": "last-col"}).text
                high = soup.find("td", {"class": "high-col"}).text
                low = soup.find("td", {"class": "low-col"}).text
                volume = soup.find("td", {"class": "volume-col"}).text
                investment = investment_and_url[symbol]
                
                update_history(investment, high, low, last_price, volume)

                investment.live_price = last_price
                investment.save()

    def update_investment_and_history(self):
        """
        Uses ASX data from BigCharts (MarketWatch) to propagate portfolio with share data.
        There is no official API so data is scraped from their website. Not sure if this
        breaks terms of use.

        This is done asynchronously to improve speed.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.scrape())