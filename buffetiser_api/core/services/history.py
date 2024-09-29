     
"""
This module contains a number of functions that can be used to get historical data for an
Investment. The functions are used by DRF to retrieve the required data to satisfy URL 
get/post calls from the front end.
"""
import datetime
from core.models import DividendReinvestment, History, Investment, Purchase, Sale
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(filename="debug.log",
                    # format='%(asctime)s %(message)s',
                    format='--------history.py----------%(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_purchase_history(investment):
    """
    All the purchases that have been made of this Investment.
    """
    investment_purchase_history = Purchase.objects.filter(investment=investment).all()
    purchases = {}
    for purchase in investment_purchase_history:
        purchases.setdefault(purchase.date.strftime("%d/%m/%Y"), []) \
            .append((purchase.units, purchase.price_per_unit, purchase.units*purchase.price_per_unit))
    return purchases

def get_sale_history(investment):
    """
    All the sales that have been made of this Investment.
    """
    investment_sale_history = Sale.objects.filter(investment=investment).all()
    sales = {}
    for sale in investment_sale_history:
        sales.setdefault(sale.date.strftime("%d/%m/%Y"), []) \
            .append((sale.units, sale.price_per_unit, sale.units*sale.price_per_unit))
    return sales

def get_total_reinvestment_units(investment):
    """
    If an Investment has recieved reinvestment units, return the total number of units
    received.
    """
    reinvestments = DividendReinvestment.objects.filter(investment=investment)
    total_reinvestment_units = 0
    for reinvestment in reinvestments:
        total_reinvestment_units += reinvestment.units
    return total_reinvestment_units

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
    all_transaction_dates.sort(key=lambda date: datetime.datetime.strptime(date, "%d/%m/%Y"))

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
    for date in credit_debit_history_by_date.keys():
        running_total += credit_debit_history_by_date[date]
        credit_debit_history[date] = running_total
        
        return credit_debit_history

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
    total_profit = (total_value := get_total_value(investment)) - \
                   (total_cost := get_total_cost(investment))
    total_profit_percentage = (total_value / total_cost -1) * 100
    return (total_profit, total_profit_percentage)

def get_daily_change(investment):
    """
    Uses ASX data from BigCharts (MarketWatch) to get daily change data.
    """
    last_update = None
    if len(History.objects.filter(investment=investment).all()) > 0:
        last_update = History.objects.filter(investment=investment).order_by('-id')[0]
    # Don't want to hammer (abuse) the service so only allow updates once a day.
    # if not last_update or last_update.date != datetime.date.today():
    print("Getting live price")
    url = 'https://bigcharts.marketwatch.com/quotes/multi.asp?view=q&msymb=' + \
        'au:{}+'.format(investment.symbol)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    daily_change = soup.find('td', {'class': 'change-col'}).text.replace("\xa0", "")
    daily_change_percent = soup.find('td', {'class': 'percent-col'}).text

    return (daily_change, daily_change_percent)
    
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
        last_update = History.objects.filter(investment=investment).order_by('-id')[0]
    # Don't want to hammer (abuse) the service so only allow updates once a day.
    if not last_update or last_update.date != datetime.date.today():
        print("Getting live price")
        url = 'https://bigcharts.marketwatch.com/quotes/multi.asp?view=q&msymb=' + \
            'au:{}+'.format(investment.symbol)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        lastPrice = soup.find('td', {'class': 'last-col'}).text
        high = soup.find('td', {'class': 'high-col'}).text
        low = soup.find('td', {'class': 'low-col'}).text
        daily_change = soup.find('td', {'class': 'change-col'}).text
        daily_change_percent = soup.find('td', {'class': 'percent-col'}).text
        volume = soup.find('td', {'class': 'volume-col'}).text

        history_entry = History(
            investment=investment,
            date=datetime.date.today(),
            high=high,
            low=low,
            close=lastPrice,
            volume=int(volume.replace(',', '')),
        )
        history_entry.save()

        return history_entry
    else:
        return last_update


def get_all_details_for_investment(investment):
    """
    Return a dictionary with all the details required by the front end to render an Investment
    entry.
    """
    history = None
    last_price = float(get_live_price(investment).close)
    if len(History.objects.filter(investment=investment).all()) > 0:
        yesterday_price = History.objects.filter(investment=investment).order_by('-id')[0].close
    else:
        yesterday_price = last_price

    daily_change = get_daily_change(investment)
    profit_total = get_profit_total_and_percentage(investment)
    all_details = {
        "name": investment.name,
        "symbol":investment.symbol,
        "yesterday_price":yesterday_price,
        "last_price":last_price,
        "variation": last_price - yesterday_price,
        "variation_percent": (last_price-yesterday_price) / yesterday_price,
        "daily_gain": daily_change[0],
        "daily_gain_percent": daily_change[1],
        "units": get_total_units_held(investment),
        "average_cost": get_average_cost(investment),
        "total_cost": get_total_cost(investment),
        "profit": profit_total[0],
        "profit_percent": profit_total[1],
    }
    return all_details