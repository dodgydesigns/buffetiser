import datetime
import json
import logging

from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup

from core.models import (DailyChange, DividendReinvestment, History,
                         Investment, Purchase)
from core.services.investment_helpers import (get_purchase_history,
                                              get_sale_history,
                                              initiate_async_scape)
from core.services.update_investment import update_history

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

    daily_change = float(daily_change_string) if daily_change_string != "UNCH" else 1.0
    daily_change_percent = (
        float(daily_change_percent_string) if daily_change_string != "UNCH" else 1.0
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


def get_all_details_for_investment(investment):
    """
    Return a dictionary with all the details required by the front end to render an Investment
    entry.

    Before this is called, the following should be called to ensure the latest data is available:
        - initiate_async_scape(scraper_function_get_daily_change)
        - initiate_async_scape(scraper_function_investment_and_history)
    """
    live_price = investment.live_price
    if len(History.objects.filter(investment=investment).all()) > 0:
        yesterday_price = (
            History.objects.filter(investment=investment).order_by("-id")[1].close
        )
    else:
        yesterday_price = live_price

    daily_change = DailyChange.objects.filter(symbol=investment.symbol).first()
    profit_total = get_profit_total_and_percentage(investment)

    all_details = {
        "name": investment.name,
        "symbol": investment.symbol,
        "yesterday_price": yesterday_price,
        "last_price": live_price,
        "variation": live_price - yesterday_price,
        "variation_percent": (live_price - yesterday_price) / yesterday_price,
        "daily_change": daily_change.daily_change,
        "daily_change_percent": daily_change.daily_change_percent,
        "units": get_total_units_held(investment),
        "average_cost": get_average_cost(investment),
        "total_cost": get_total_cost(investment),
        "profit": profit_total[0],
        "profit_percent": profit_total[1],
        "history": get_investment_price_history(investment),
    }
    return all_details


def get_investment_price_history(investment):
    """
    Return a list of the daily details of an Investment: low, high, close and volume. Used to create a
    plot of the history of an Investment's value.
    """
    investment_price_history = {}
    for history in list(History.objects.filter(investment=investment)):
        investment_price_history[history.date.strftime("%Y%m%d")] = {
            "low": history.low,
            "high": history.high,
            "close": history.close,
            "volume": history.volume,
        }
    return investment_price_history


def get_credit_debit_history():
    """
    Generates the money put into (purchases) and removed (sales) by date for all Investments.
    """
    investments = Investment.objects.all()
    purchases = {}
    sales = {}
    for investment in investments:
        purchases.update(get_purchase_history(investment))
        sales.update(get_sale_history(investment))

    all_transaction_dates = list(set(list(purchases.keys()) + list(sales.keys())))
    all_transaction_dates.sort(
        key=lambda date: datetime.datetime.strptime(date, "%d/%m/%Y")
    )

    credit_debit_history_by_date = {}
    total = 0
    for date in all_transaction_dates:
        if date in purchases:
            total += purchases[date][0][2]
        if date in sales:
            total -= sales[date][0][2]
        credit_debit_history_by_date[date] = total

    return credit_debit_history_by_date


def get_total_units_held(investment):
    """
    Get the number of units held of a particular investment.
    """
    units_held = 0
    purchases = get_purchase_history(investment).values()
    for purchase in purchases:
        units_held += int(purchase[0][0])

    reinvestment_units = get_total_reinvestment_units(investment)
    units_held += reinvestment_units

    sales = get_sale_history(investment)
    for sale in sales:
        units_held -= int(sale[0][0])
    return units_held


def get_total_cost(investment):
    """
    The sum of all purchases of an investment.
    """
    purchases = Purchase.objects.filter(investment=investment).all()
    total_cost = 0
    for purchase in purchases:
        total_cost += purchase.price_per_unit * purchase.units
    return total_cost


def get_total_value(investment):
    """
    The current total value of an investment.
    """
    # Make sure live price and history are the latest values.
    # update_investment_and_history()
    # Get the latest History entry
    return get_total_units_held(investment) * float(
        list(History.objects.filter(investment=investment))[-1].close
    )


def get_average_cost(investment):
    """
    The average cost per unit of an investment.
    """
    return get_total_cost(investment) / get_total_units_held(investment)


def get_profit_total_and_percentage(investment):
    """
    Return the profit in dollars and as a percent.
    """
    total_profit = (total_value := get_total_value(investment)) - (
        total_cost := get_total_cost(investment)
    )
    total_profit_percentage = (total_value / total_cost - 1) * 100
    return (total_profit, total_profit_percentage)


def get_total_reinvestment_units(investment):
    """
    If an Investment has received reinvestment units, return the total number of units
    received.
    """
    reinvestments = DividendReinvestment.objects.filter(investment=investment)
    total_reinvestment_units = 0
    for reinvestment in reinvestments:
        total_reinvestment_units += reinvestment.units
    return total_reinvestment_units
