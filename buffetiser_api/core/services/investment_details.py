import datetime
import json
import logging

from bs4 import BeautifulSoup

from core.models import DividendReinvestment, History, Investment, Purchase
from core.services.investmet_helpers import get_purchase_history, get_sale_history
from core.services.update_investment import update_investment_and_history

logging.basicConfig(
    filename="debug.log",
    # format='%(asctime)s %(message)s',
    format="--------update_investment.py----------%(message)s",
    filemode="w",
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_daily_change(investment):
    """
    Uses ASX data from BigCharts (MarketWatch) to get daily change data.
    """
    if len(History.objects.filter(investment=investment).all()) > 0:
        last_update = History.objects.filter(investment=investment).order_by("-id")[0]
    # Don't want to hammer (abuse) the service so only allow updates once a day.
    daily_change = None
    daily_change_percent = None
    if not last_update or last_update.date != datetime.date.today():
        logger.log(f"Getting live price for {investment.symbol}")
        url = f"https://bigcharts.marketwatch.com/quotes/multi.asp?view=q&msymb=au:{investment.symbol}+"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        daily_change = soup.find("td", {"class": "change-col"}).text.replace("\xa0", "")
        daily_change_percent = soup.find("td", {"class": "percent-col"}).text

    return {"daily_change": daily_change, "daily_change_percent": daily_change_percent}


def get_all_details_for_investment(investment):
    """
    Return a dictionary with all the details required by the front end to render an Investment
    entry.
    """
    # update_investment_and_history()
    live_price = investment.live_price
    if len(History.objects.filter(investment=investment).all()) > 0:
        yesterday_price = (
            History.objects.filter(investment=investment).order_by("-id")[0].close
        )
    else:
        yesterday_price = live_price

    daily_change = get_daily_change(investment)
    profit_total = get_profit_total_and_percentage(investment)
    all_details = {
        "name": investment.name,
        "symbol": investment.symbol,
        "yesterday_price": yesterday_price,
        "last_price": live_price,
        "variation": live_price - yesterday_price,
        "variation_percent": (live_price - yesterday_price) / yesterday_price,
        "daily_change": daily_change["daily_change"] if daily_change["daily_change"] else 0,
        "daily_change_percent": daily_change["daily_change_percent"] if daily_change["daily_change_percent"] else 0,
        "units": get_total_units_held(investment),
        "average_cost": get_average_cost(investment),
        "total_cost": get_total_cost(investment),
        "profit": profit_total[0],
        "profit_percent": profit_total[1],
    }
    return all_details


def get_details_for_all_investments():
        """
        Get the details for all Investments as JSON.
        """
        all_investment_details= []
        for investment in Investment.objects.all():
            all_investment_details.append(get_all_details_for_investment(investment))
        return json.dumps(all_investment_details)


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
    return get_total_units_held(investment) * float(list(History.objects.filter(investment=investment))[-1].close)


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
