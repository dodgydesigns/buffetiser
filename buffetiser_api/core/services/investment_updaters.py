"""
main.py
====================================
The core module of my example project currentmodule
"""

def about_me(your_name):
    """
    Return the most important thing about a person.

    Parameters
    ----------
    your_name
        A string indicating the name of the person.

    """
    return "The wise {} loves Python.".format(your_name)


class ExampleClass:
    """An example docstring for a class definition."""

    def __init__(self, name):
        """
        Blah blah blah.

        Parameters
        ---------
        name
            A string to assign to the `name` instance attribute.

        """
        self.name = name

    def about_self(self):
        """
        Return information about an instance created from ExampleClass.
        """
        return "I am a very smart {} object.".format(self.name)
    
    
    
    
"""
All the functions to update values for Investments.
"""

import datetime
import logging
from math import floor

from core.models import DividendPayment, DividendReinvestment, History
from core.services.investment_helpers import get_units_held_at_date

logging.basicConfig(
    filename="debug.log",
    # format='%(asctime)s %(message)s',
    format="--------update_investment.py----------%(message)s",
    filemode="w",
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


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
            History.objects.filter(
                date=nearest(price_history_list, cutoff_date), investment=investment
            )
            .first()
            .close
        )
    if reinvest:
        # Can we afford one or more shares (based on cutoff price and the amount of money we were paid?)
        #     money we were paid        cost of one share at cutoff
        if (units_held * price_per_unit) >= nearest_value_to_cutoff:
            reinvestment_units_received = int(
                floor((units_held * price_per_unit) / nearest_value_to_cutoff)
            )
            reinvestment = DividendReinvestment(
                reinvestment_date=reinvestment_date,
                units=reinvestment_units_received,
                investment=investment,
            )
            # Once we have bought all the full shares we can afford, handle the leftover money
            left_over = (units_held * price_per_unit) - (
                reinvestment_units_received * nearest_value_to_cutoff
            )
            dividend_payment = DividendPayment(
                payment_date=reinvestment_date, value=left_over, investment=investment
            )
            reinvestment.save()
            dividend_payment.save()
        else:
            dividend_payment = DividendPayment(
                payment_date=reinvestment_date,
                value=(units_held * price_per_unit),
                investment=investment,
            )
            dividend_payment.save()
    else:
        dividend_payment = DividendPayment(
            payment_date=reinvestment_date,
            value=(units_held * price_per_unit),
            investment=investment,
        )
        dividend_payment.save()
        # TODO: Put the money in Financial as well


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
            volume= 0 if volume == "n/a" else int(volume.replace(",", "")),
        )
        history_entry.save()


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
