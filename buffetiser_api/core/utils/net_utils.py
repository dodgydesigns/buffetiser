from django.utils import timezone
import requests
from bs4 import BeautifulSoup

from core import models


def use_big_charts(investment):
    """
    Uses ASX data from BigCharts (MarketWatch) to propagate portfolio with share data.
    There is no official API so data is scraped from their website. Not sure if this
    breaks terms of use.
    :param investment: The Investment object that provides details to look up.
    :return history_data: An dict that can be added to an Investment or
    interrogated for parameters.
    """

    url = (
        "https://bigcharts.marketwatch.com/quotes/multi.asp?view=q&msymb="
        + f"au:{investment.symbol}+"
    )
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    date = timezone.now()
    high = float(soup.find("td", {"class": "high-col"}).text)
    low = float(soup.find("td", {"class": "low-col"}).text)
    close = float(soup.find("td", {"class": "last-col"}).text)
    volume = int(soup.find("td", {"class": "volume-col"}).text.replace(",", ""))

    history_data = {
        "user": investment.user,
        "investment": investment,
        "date": date,
        "high": round(high * 100, 2),
        "low": round(low * 100, 2),
        "close": round(close * 100, 2),
        "volume": volume,
    }

    return history_data


def update_history(investment):
    """Determine if the last time an update was called is at least 24 hours. This ensures that
    the history is day values and that the price server isn't hit too often. If so, an History
    object is created for the investment."""

    return_message = ""
    history_data = None
    history_list = models.History.objects.filter(investment=investment).order_by("date")

    if len(history_list) > 0:
        latest_history_date = history_list[0].date
        time_diff = timezone.now() - latest_history_date
        if time_diff.days >= 1:
            history_data = use_big_charts(investment)
            return_message = f"Added History entry for {investment.symbol}."
    elif len(history_list) == 0:
        history_data = use_big_charts(investment)
        return_message = f"Created first History entry for {investment.symbol}."
    else:
        return_message = "No update required."

    if history_data:
        history_entry = models.History.objects.create(
            user=investment.user,
            investment=investment,
            date=history_data["date"],
            high=round(history_data["high"] * 100, 2),
            low=round(history_data["low"] * 100, 2),
            close=round(history_data["close"] * 100, 2),
            volume=history_data["volume"],
        )
        history_entry.save()

    print_stuff(investment, history_list[0])
    return return_message


def print_stuff(investment, history_entry):
    """Debugging function to see what's being returned"""
    print(investment.name)
    print(f"user: {history_entry.user}")
    print(f"date: {history_entry.date}")
    print(f"high: {history_entry.high}")
    print(f"low: {history_entry.low}")
    print(f"close: {history_entry.close}")
    print(f"volume: {history_entry.volume}")
    print("\n")
