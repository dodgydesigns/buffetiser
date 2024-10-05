"""
All the functions to update values for Investments.
"""
import datetime
import logging
from math import floor

import requests
from bs4 import BeautifulSoup

from core.models import (DividendPayment, DividendReinvestment, History,
                         Investment, Purchase, Sale)

logging.basicConfig(
    filename="debug.log",
    # format='%(asctime)s %(message)s',
    format="--------update_investment.py----------%(message)s",
    filemode="w",
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def update_all_investment_prices():
    """
    Get today's prices for all investment to add to History.
    NOTE: This could be added as a Command and run as CRON job.
    """
    for  trade_count, investment in enumerate(Investment.objects.all()):
        get_live_price(investment)


def get_live_price(investment):
    """
    Uses ASX data from BigCharts (MarketWatch) to propagate portfolio with share data.
    There is no official API so data is scraped from their website. Not sure if this
    breaks terms of use.
    :param: The investment to fetch data for.
    :param todayString: The date for today.
    """
    last_update = None
    if len(History.objects.filter(investment=investment).all()) > 0:
        last_update = History.objects.filter(investment=investment).order_by("-id")[0]
    # Don't want to hammer (abuse) the service so only allow updates once a day.
    if not last_update or last_update.date != datetime.date.today():
        print(f"Getting live price: {investment.symbol}")
        history_entry = None
        last_update = None
        try:
            url = f"https://bigcharts.marketwatch.com/quotes/multi.asp?view=q&msymb=au:{investment.symbol}+"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            last_price = soup.find("td", {"class": "last-col"}).text
            high = soup.find("td", {"class": "high-col"}).text
            low = soup.find("td", {"class": "low-col"}).text
            volume = soup.find("td", {"class": "volume-col"}).text

            update_history(investment, high, low, last_price, volume)

            investment.live_price = last_price
            investment.save()
        except requests.exceptions.HTTPError as e:
            print(f"Couldn't get data for {investment.symbol}: {e}")
        return history_entry
    else:
        return last_update


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
    last_price = float(get_live_price(investment).close)
    if len(History.objects.filter(investment=investment).all()) > 0:
        yesterday_price = (
            History.objects.filter(investment=investment).order_by("-id")[0].close
        )
    else:
        yesterday_price = last_price

    daily_change = get_daily_change(investment)
    profit_total = get_profit_total_and_percentage(investment)
    all_details = {
        "name": investment.name,
        "symbol": investment.symbol,
        "yesterday_price": yesterday_price,
        "last_price": last_price,
        "variation": last_price - yesterday_price,
        "variation_percent": (last_price - yesterday_price) / yesterday_price,
        "daily_change": daily_change["daily_change"],
        "daily_change_percent": daily_change["daily_change_percent"],
        "units": get_total_units_held(investment),
        "average_cost": get_average_cost(investment),
        "total_cost": get_total_cost(investment),
        "profit": profit_total[0],
        "profit_percent": profit_total[1],
    }
    return all_details


###     History Related Stuff ###
def nearest(items, pivot):
    """
    Find the nearest item (date) in a list.
    """
    return min(items, key=lambda x: abs(x - pivot.date()))


def add_dividend(investment, reinvest, cutoff_date, reinvestment_date, price_per_unit):
    """
    Inputs: investment: Investment
            reinvest: whether re-investment is enabled for this Investment
            cutoff_date: the date the dividend price per unit is determined
            reinvestment_date: the date the dividend was paid
            units: the number of units of that Investment held at cutoff_date
            price_per_unit: the price per unit paid out

    A dividend can be either paid out or re-invested.
    Payout: no reinvestment plan setup, dividend is not enough to buy 1 share.
    (add dividend value to Financials).
    Reinvest: re-investment plan setup, dividend is enough to buy 1 or more shares.
    """
    # Price per unit is given is cents so convert to dollars
    price_per_unit = price_per_unit / 100
    reinvestment_date = datetime.datetime.strptime(reinvestment_date, "%d/%m/%Y")
    cutoff_date = datetime.datetime.strptime(cutoff_date, "%d/%m/%Y")
    # The units held at the time of the cutoff date
    units_held = get_units_held_at_date(investment, cutoff_date)
    # If there is a list of History objects, try and get the price that is closest to the
    # cut_off date. Otherwise, just grab the latest price.
    price_history_list = [
        history.date for history in History.objects.filter(investment=investment).all()
    ]
    nearest_history_date_to_cutoff = nearest(price_history_list, cutoff_date)
    if len(price_history_list) > 0 and nearest_history_date_to_cutoff:
        nearest_value_to_cutoff = (
            History.objects.filter(date=nearest(price_history_list, cutoff_date), investment=investment)
            .first()
            .close
        )
    if reinvest:
        # Can we afford one or more shares (based on cutoff price and the amount of money we were paid?)
        #     money we were paid        cost of one share at cutoff
        if (units_held * price_per_unit) >= nearest_value_to_cutoff:
            reinvestment_units_received = int(floor((units_held * price_per_unit) / nearest_value_to_cutoff))
            reinvestment = DividendReinvestment(reinvestment_date=reinvestment_date, 
                                                units=reinvestment_units_received, 
                                                investment=investment)
            # Once we have bought all the full shares we can afford, handle the leftover money
            left_over = (units_held * price_per_unit) - (reinvestment_units_received * nearest_value_to_cutoff)
            dividend_payment = DividendPayment(payment_date=reinvestment_date, 
                                               value=left_over, 
                                               investment=investment)
            reinvestment.save()
            dividend_payment.save()
        else:
            dividend_payment = DividendPayment(payment_date=reinvestment_date, 
                                               value=(units_held * price_per_unit), 
                                               investment=investment)
            dividend_payment.save()
    else:
        dividend_payment = DividendPayment(payment_date=reinvestment_date, 
                                           value=(units_held * price_per_unit), 
                                           investment=investment)
        dividend_payment.save()
        # TODO: Put the money in Financial as well


def update_history(investment, high, low, last_price, volume):
    """
    Add a new element to the History record.
    """
    history_entry = History(
        investment=investment,
        date=datetime.datetime.now(),
        high=high,
        low=low,
        close=last_price,
        volume=int(volume.replace(",", "")),
    )
    history_entry.save()


def get_purchase_history(investment):
    """
    All the purchases that have been made of this Investment.
    """
    investment_purchase_history = Purchase.objects.filter(investment=investment).all()
    purchases = {}
    for purchase in investment_purchase_history:
        purchases.setdefault(purchase.date.strftime("%d/%m/%Y"), []).append(
            (
                purchase.units,
                purchase.price_per_unit,
                purchase.units * purchase.price_per_unit,
            )
        )
    return purchases


def get_sale_history(investment):
    """
    All the sales that have been made of this Investment.
    """
    investment_sale_history = Sale.objects.filter(investment=investment).all()
    sales = {}
    for sale in investment_sale_history:
        sales.setdefault(sale.date.strftime("%d/%m/%Y"), []).append(
            (sale.units, sale.price_per_unit, sale.units * sale.price_per_unit)
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
    all_transaction_dates.sort(
        key=lambda date: datetime.datetime.strptime(date, "%d/%m/%Y")
    )

    credit_debit_history_by_date = {}
    for date in all_transaction_dates:
        total = 0
        if date in purchases:
            total += purchases[date][0][2]
        if date in sales:
            total -= sales[date][0][2]
        credit_debit_history_by_date[date] = total

    running_total = 0
    credit_debit_history = {}
    for date, value in credit_debit_history_by_date.items():
        running_total += value
        credit_debit_history[date] = running_total

        return credit_debit_history


def get_units_held_at_date(investment, cut_off_date):
    """
    This gets all the units held for an Investment up to (and including) a certain date.
    """
    purchases = get_purchase_history(investment)
    sales= get_sale_history(investment)

    units_held_at_date = 0
    for purchase_date in list(purchases.keys()):
        if datetime.datetime.strptime(purchase_date, "%d/%m/%Y") <= cut_off_date:
            # import pdb; pdb.set_trace()
            units_held_at_date += purchases[purchase_date][0][0]
    for sales_date in list(sales.keys()):
        if datetime.datetime.strptime(sales_date, "%d/%m/%Y") <= cut_off_date:
            units_held_at_date -= purchases[purchase_date][0][0]

    return int(units_held_at_date)
    

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
    return get_total_units_held(investment) * get_live_price(investment).close


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


def get_plot_data(investment):
    """
    Return the history data: low, high, close for an investment. Used to plot value history.
    """
    history = History.objects.filter(investment=investment).all()
    history_dict = {}
    for day in history:
        print(day.date)
        history_dict[day.date.strftime("%d/%m/%Y")] = (day.low, day.high, day.close)

    return history_dict
