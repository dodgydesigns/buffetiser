import datetime
from core.models import Purchase, Sale


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
