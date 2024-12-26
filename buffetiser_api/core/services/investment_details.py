import datetime
import json
import logging

from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from core.models import DailyChange, DividendReinvestment, History, Investment, Purchase
from core.services.investment_helpers import (
    date_to_datetime,
    date_to_string,
    get_purchase_history,
    get_purchase_history,
    get_sale_history,
    get_sale_history,
)
from core.services.investment_updaters import update_history

logging.basicConfig(
    filename="debug.log",
    # format='%(asctime)s %(message)s',
    format="--------investment_details.py----------%(message)s",
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


def get_all_details_for_investment(investment):
    """
    Return a dictionary with all the details required by the front end to render an Investment
    entry.

    Before this is called, the following should be called to ensure the latest data is available:
        - initiate_async_scape(scraper_function_get_daily_change)
        - initiate_async_scape(scraper_function_investment_and_history)
    """
    date = datetime.datetime.now()
    live_price = investment.live_price
    if len(History.objects.filter(investment=investment).all()) > 0:
        yesterday_price = (
            History.objects.filter(investment=investment).order_by("-id")[1].close
        )
    else:
        yesterday_price = live_price

    variation = DailyChange.objects.filter(symbol=investment.symbol).first()
    profit_total = get_profit_total_and_percentage_on_date(investment, date)

    all_details = {
        "name": investment.name,
        "symbol": investment.symbol,
        "last_price": live_price,
        "variation": live_price - yesterday_price,
        "daily_change": variation.daily_change if variation else 0,
        "daily_change_percent": variation.daily_change_percent if variation else 0,
        "units": get_total_units_held_on_date(investment, date),
        "average_cost": get_average_cost_on_date(investment, date),
        "total_cost": get_total_cost_on_date(investment, date),
        "profit": profit_total["total_profit"],
        "profit_percent": profit_total["total_profit_percentage"],
        "history": get_investment_price_history(investment),
        "credit_debit_history": get_credit_debit_history(),
    }
    return all_details


def get_investment_price_history(investment):
    """
    Return a list of the daily details of an Investment: low, high, close and volume. Used to create a
    plot of the history of an Investment's value.
    """
    price_history = []
    for history in list(History.objects.filter(investment=investment)):
        price_history.append(
            {
                "date": history.date,
                "low": history.low,
                "high": history.high,
                "close": history.close,
                "volume": history.volume,
            }
        )
    return price_history


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
        key=lambda date: date
    )

    credit_debit_history_by_date = []
    total = 0
    for date in all_transaction_dates:
        if date in purchases.keys():
            for purchase in purchases[date]:
                total += purchase["total_cost"]
        if date in sales.keys():
            for sale in sales[date]:
                total -= sale["total_cost"]
        credit_debit_history_by_date.append({"date": date, "total": total})

    return credit_debit_history_by_date


def get_total_units_held_on_date(investment, date):
    """
    Get the number of units held of a particular investment on a 
    certain date.
    """
    units_held = 0
    purchases_dict = get_purchase_history(investment).items()
    for purchase_date, purchases in purchases_dict:
        for purchase in purchases:
            # There can be multiple purchases per day.
            if date_to_datetime(purchase_date) <= date:
                units_held += int(purchase["units"])

    reinvestment_units = get_total_reinvestment_units_on_date(investment, date)
    units_held += reinvestment_units

    sales_dict = get_sale_history(investment).items()
    for sale_date, sales in sales_dict:
        # There can be multiple sales per day.
        for sale in sales:
            if date_to_datetime(sale_date) <= date:
                units_held -= int(sale["units"])

    return units_held


def get_total_cost_on_date(investment, date):
    """
    The sum of all purchases of an investment.
    """
    purchases = Purchase.objects.filter(investment=investment).all()
    total_cost = 0
    for purchase in purchases:
        if date_to_datetime(purchase.date) <= date:
            total_cost += purchase.price_per_unit * purchase.units
    return total_cost


def get_total_value_on_date(investment, date):
    """
    The current total value of an investment.
    """
    total_value_on_date = 0
    if len(list(History.objects.filter(investment=investment))) >= 1:
        total_value_on_date = get_total_units_held_on_date(investment, date) * float(
            list(History.objects.filter(investment=investment))[-1].close
        )
    return total_value_on_date


def get_average_cost_on_date(investment, date):
    """
    The average cost per unit of an investment.
    """
    # We can have zero units held if the Investment is just being watched
    total_cost_on_date = 0
    if get_total_units_held_on_date(investment, date) > 0:
        total_cost_on_date = get_total_cost_on_date(investment, date) / get_total_units_held_on_date(investment, date)
    return total_cost_on_date


def get_profit_total_and_percentage_on_date(investment, date):
    """
    Return the profit in dollars and as a percent.
    """
    # We can have zero value if the Investment is just being watched
    total_profit = 0
    total_profit_percentage = 0
    total_value = get_total_value_on_date(investment, date)
    total_cost = get_total_cost_on_date(investment, date)
    if total_value > 0 and total_cost > 0:
        total_profit = total_value - total_cost
        total_profit_percentage = ((total_value / total_cost) - 1) * 100
    return {"total_profit": total_profit, "total_profit_percentage": total_profit_percentage}


def get_total_reinvestment_units_on_date(investment, date):
    """
    If an Investment has received reinvestment units, return the total number of units
    received.
    """
    reinvestments = DividendReinvestment.objects.filter(investment=investment)
    total_reinvestment_units = 0
    for reinvestment in reinvestments:
        if date_to_datetime(reinvestment.reinvestment_date) <= date:
            total_reinvestment_units += reinvestment.units
    return total_reinvestment_units


def get_portfolio_value_history():
    """
    Get the value of all shares for each date for the whole portfolio.
    """
    # TODO: List of dividends reinvested ***

    date = datetime.datetime.now()

    # Remove duplicate history dates
    history_dates = set()
    # Declaring this here make the search faster: Python is a 
    # dynamic language, and resolving history_dates.add each iteration is more costly than resolving a local variable.
    history_dates_add = history_dates.add   
    history_dates = [history.date for history in History.objects.all().order_by("date") 
                     if not (history.date in history_dates or history_dates_add(history.date))]
    history_start_date = history_dates[0]

    purchases_dict = {}
    sales_dict = {}
    for investment in Investment.objects.all():
        purchases_dict.update(get_purchase_history(investment))
        sales_dict.update(get_sale_history(investment))

    # Purchase happened before history started: units*price_per_unit #TODO: This could be a separate chart
    # but doesn't fit in well with the history chart.
    pre_history_value_on_date = {}
    # cumulative_value = 0
    # for purchase_date in sorted(purchases_dict.keys()):
    #     pre_history_value_on_date[date_to_string(purchase_date)] = 0
    #     if purchase_date < history_start_date:
    #         for purchase in purchases_dict[purchase_date]:
    #             cumulative_value += int(purchase["units"]) * float(purchase["price_per_unit"])
    #             pre_history_value_on_date[date_to_string(purchase_date)] = cumulative_value

    # Purchase happened after history started: unit*close
    history_value_on_date = {}
    for history_date in history_dates:
        cumulative_value = 0
        history_value_on_date[date_to_string(history_date)] = 0
        close_value = 0
        for investment in Investment.objects.all():
            units = get_total_units_held_on_date(investment, date_to_datetime(history_date))
            # We can have zero History if we are just watching the Investment
            if len(History.objects.filter(investment=investment, date=history_date)) > 0:
                close_value = History.objects.filter(investment=investment, date=history_date).first().close
            cumulative_value += units * close_value
        history_value_on_date[date_to_string(history_date)] = cumulative_value

    value_history_dict = pre_history_value_on_date
    value_history_dict.update(history_value_on_date)

    value_history = []
    for date, total in value_history_dict.items():
        value_history.append({"date": date, "total": total})
    return value_history


def get_portfolio_totals():
    """
    Get the profit and percent profit for the whole portfolio.
    """
    date = datetime.datetime.now()
    
    portfolio = {"total_cost":0, "total_profit": 0, "total_profit_percentage": 0, "total_value": 0,}
    for investment in Investment.objects.all():
        investment_cost = get_total_cost_on_date(investment, date)
        investment_profit = get_profit_total_and_percentage_on_date(investment, date)["total_profit"]
        investment_value = get_total_value_on_date(investment, date)
        portfolio["total_cost"] += investment_cost
        portfolio["total_profit"] += investment_profit
        portfolio["total_value"] += investment_value

    portfolio["total_profit_percentage"] = ((portfolio["total_value"] / portfolio["total_cost"]) -1 ) * 100

    return portfolio