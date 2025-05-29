import datetime
from functools import cache
import logging

from django.db.models import Sum

from core.models import (DailyChange, DividendReinvestment, History,
                         Investment, Purchase, Sale)
from core.services.investment_helpers import (date_to_datetime, date_to_string,)

logging.basicConfig(
    filename="debug.log",
    # format='%(asctime)s %(message)s',
    format="--------investment_details.py----------%(message)s",
    filemode="w",
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


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
    if (History.objects.filter(investment=investment)
        and len(History.objects.filter(investment=investment).all()) > 0):
        yesterday_price = (History.objects.filter(investment=investment).order_by("-id")[1].close)
    else:
        yesterday_price = live_price

    variation = DailyChange.objects.filter(symbol=investment.symbol).first()
    profit_total = get_profit_total_and_percentage_on_date(investment, date)

    all_details = {
        "name": investment.name,
        "symbol": investment.symbol,
        "visible": investment.visible,
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


def get_purchase_history(investment):
    """
    All the purchases that have been made of this Investment.
    """
    investment_purchase_history = Purchase.objects.filter(investment=investment).all()
    purchases = {}
    for purchase in investment_purchase_history:
        purchases.setdefault(purchase.date, []).append(
            {
                "units": purchase.units,
                "price_per_unit": purchase.price_per_unit,
                "total_cost": purchase.units * purchase.price_per_unit,
            }
        )
    return purchases


def get_sale_history(investment):
    """
    All the sales that have been made of this Investment.
    """
    investment_sale_history = Sale.objects.filter(investment=investment).all()
    sales = {}
    for sale in investment_sale_history:
        sales.setdefault(sale.date, []).append(
            {
                "units": sale.units,
                "price_per_unit": sale.price_per_unit,
                "total_cost": sale.units * sale.price_per_unit,
            }
        )
    return sales


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
    all_transaction_dates.sort(key=lambda date: date)

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


@cache
def get_total_units_held_on_date(investment, date):
    """
    Get the number of units held of a particular investment on a
    certain date.
    """

    purchases_units = Purchase.objects.filter(investment=investment, 
                                              date__lte=date).aggregate(total=Sum('units'))['total'] or 0
    reinvestments_units = DividendReinvestment.objects.filter(investment=investment, 
                                                              date__lte=date).aggregate(total=Sum('units'))['total'] or 0
    sales_units = Sale.objects.filter(investment=investment, 
                                      date__lte=date).aggregate(total=Sum('units'))['total'] or 0

    units_held = purchases_units + reinvestments_units - sales_units

    return units_held


def get_average_cost_on_date(investment, date):
    """
    The average cost per unit of an investment.
    """
    # We can have zero units held if the Investment is just being watched
    total_cost_on_date = 0
    total_units_held_on_date = get_total_units_held_on_date(investment, date)
    if total_units_held_on_date > 0:
        total_cost_on_date = get_total_cost_on_date(investment, date) / total_units_held_on_date
    return total_cost_on_date


@cache
def get_total_cost_on_date(investment, date):
    """
    The formula for the total cost of an Investment on a certain date as used by the ATO for shares held over 12 months is:
    Sum of all purchase costs*units, adding re-investment units and subtracting sales*average cost.
    For shares held less than 12 months, the FIFO (First In First Out) method is used.
    """
    purchases = Purchase.objects.filter(investment=investment, date__lte=date).all()
    purchases_cost = 0
    purchase_units = 0
    for purchase in purchases:
        purchase_units += purchase.units
        purchases_cost += purchase.price_per_unit * purchase.units

    reinvestment_units = DividendReinvestment.objects.filter(investment=investment, 
                                                             date__lte=date).aggregate(total=Sum('units'))['total'] or 0
    sales_units = Sale.objects.filter(investment=investment, 
                                      date__lte=date).aggregate(total=Sum('units'))['total'] or 0
    
    average_purchase_cost = purchases_cost / (purchase_units + reinvestment_units)
    sales_cost = sales_units * average_purchase_cost
    cost_of_currently_held = purchases_cost - sales_cost

    return cost_of_currently_held


def get_total_value_on_date(investment, date):
    """
    The current total value of an investment:
        The number of units held on a certain date multiplied by the price of the Investment on that date.
    """
    # Get the last history entry on or before the date
    closest_history_object = list(History.objects.filter(investment=investment, date__lte=date))[-1]
    closest_date = closest_history_object.date
    closest_units_to_date = get_total_units_held_on_date(investment, closest_date)
    closest_close_value_to_date = closest_history_object.close
    total_value_on_date = closest_units_to_date * closest_close_value_to_date

    return total_value_on_date


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
    return {
        "total_profit": total_profit,
        "total_profit_percentage": total_profit_percentage,
    }


def get_portfolio_value_history():
    """
    Get the value of all shares for each date for the whole portfolio.
    """
    # Get all unique history dates in order
    all_histories = History.objects.all().order_by("date").select_related("investment")
    history_dates = sorted(set(history.date for history in all_histories))
    if not history_dates:
        return []

    # Cache purchases and sales once
    purchases_dict = {}
    sales_dict = {}
    for investment in Investment.objects.all():
        purchases_dict.update(get_purchase_history(investment))
        sales_dict.update(get_sale_history(investment))

    # Group histories by (investment, date) for fast lookup
    history_lookup = {(history.investment.symbol, history.date): history.close for history in all_histories}

    # Compute portfolio value for each date
    history_value_on_date = {}
    investments = list(Investment.objects.all())  # cache for reuse
    for history_date in history_dates:
        total_value = 0
        dt = date_to_datetime(history_date)
        for investment in investments:
            units = get_total_units_held_on_date(investment, dt)
            close = history_lookup.get((investment.symbol, history_date), 0)
            total_value += units * close
        history_value_on_date[date_to_string(history_date)] = total_value

    # Format as list of dicts
    return [{"date": date, "total": total} for date, total in history_value_on_date.items()]


def get_portfolio_totals():
    """
    Get the profit and percent profit for the whole portfolio.
    """
    date = datetime.datetime.now()

    portfolio = {
        "total_cost": 0,
        "total_profit": 0,
        "total_profit_percentage": 0,
        "total_value": 0,
    }
    for investment in Investment.objects.all():
        investment_cost = get_total_cost_on_date(investment, date)
        investment_profit = get_profit_total_and_percentage_on_date(investment, date)["total_profit"]
        investment_value = get_total_value_on_date(investment, date)
        portfolio["total_cost"] += investment_cost
        portfolio["total_profit"] += investment_profit
        portfolio["total_value"] += investment_value

    portfolio["total_profit_percentage"] = ((portfolio["total_value"] / portfolio["total_cost"]) - 1) * 100

    return portfolio
