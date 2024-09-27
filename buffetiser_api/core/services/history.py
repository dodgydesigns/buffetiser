     
"""
This module contains a number of functions that can be used to get historical data for an
Investment. The functions are used by DRF to retrieve the required data to satisfy URL 
get/post calls from the front end.
"""
from datetime import datetime
from core.models import Investment, Purchase, Sale


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
    all_transaction_dates.sort(key=lambda date: datetime.strptime(date, "%d/%m/%Y"))

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
