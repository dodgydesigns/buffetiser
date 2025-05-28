"""
All the functions to update values for Investments.
"""

import datetime
import logging
from math import floor

from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup

from core.models import (DailyChange, History,)

logging.basicConfig(
    filename="debug.log",
    # format='%(asctime)s %(message)s',
    format="--------update_investment.py----------%(message)s",
    filemode="w",
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@sync_to_async
def scraper_function_get_daily_change(investment_and_url, response):
    """
    This function is passed to the scraper functions that will asynchronously iterate through
    Investments, pull the data from the Investments URLs and provide the data required below.
    The results are stored in global so they can be pulled whenever required (this seems wrong).

    To execute: initiate_async_scape(scraper_function_get_daily_change)
    Does not need to implement a loop of Investments. The async functions do this.
    """
    soup = BeautifulSoup(response, "html.parser")
    symbol = soup.find("td", {"class": "symb-col"}).text
    daily_change_string = soup.find("td", {"class": "change-col"}).text.replace(
        "\xa0", ""
    )
    daily_change_percent_string = soup.find(
        "td", {"class": "percent-col"}
    ).text.replace("%", "")

    daily_change = float(daily_change_string) if daily_change_string != "UNCH" else 0
    daily_change_percent = (
        float(daily_change_percent_string) if daily_change_string != "UNCH" else 0
    )

    daily_change = DailyChange.objects.create(
        symbol=investment_and_url[symbol]["investment"].symbol,
        daily_change=daily_change,
        daily_change_percent=daily_change_percent,
    )

    daily_change.save()


@sync_to_async
def scraper_function_investment_and_history(investment_and_url, response):
    """
    This function is passed to the scraper functions that will asynchronously iterate through
    Investments, pull the data from the Investments URLs and provide the data required below.

    To execute: initiate_async_scape(scraper_function_investment_and_history)
    Does not need to implement a loop of Investments. The async functions do this.
    """
    soup = BeautifulSoup(response, "html.parser")
    symbol = soup.find("td", {"class": "symb-col"}).text
    last_price = soup.find("td", {"class": "last-col"}).text
    high = soup.find("td", {"class": "high-col"}).text
    low = soup.find("td", {"class": "low-col"}).text
    volume = soup.find("td", {"class": "volume-col"}).text
    investment = investment_and_url[symbol]["investment"]
    update_history(investment, high, low, last_price, volume)

    investment.live_price = last_price
    investment.save()


def update_history(investment, high, low, last_price, volume):
    """
    Add a new element to the History record.
    """
    (today := datetime.date.today())
    if today not in [
        history_object.date
        for history_object in list(History.objects.filter(investment=investment))
    ]:
        history_entry = History(
            investment=investment,
            date=today,
            high=high,
            low=low,
            close=last_price,
            volume=0 if volume == "n/a" else int(volume.replace(",", "")),
        )
        history_entry.save()