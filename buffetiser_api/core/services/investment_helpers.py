import asyncio
import datetime

import aiohttp
from asgiref.sync import sync_to_async
from core.models import Investment, Purchase, Sale


def date_to_string(date):
    """Ensure all dates are formatted the same."""
    return datetime.datetime.strftime("%d/%m/%Y")

def date_to_datetime(date):
    """Ensure all dates are formatted the same."""
    return datetime.datetime(date.year, date.month, date.day)

def string_to_date(date_string):
    """Ensure all dates are formatted the same."""
    return datetime.datetime.strptime(date_string, "%d/%m/%Y")


def get_purchase_history(investment):
    """
    All the purchases that have been made of this Investment.
    """
    investment_purchase_history = Purchase.objects.filter(investment=investment).all()
    purchases = {}
    for purchase in investment_purchase_history:
        purchases.setdefault(purchase.date, []).append(
            {"units": purchase.units,
             "price_per_unit": purchase.price_per_unit,
             "total_cost": purchase.units * purchase.price_per_unit,}
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
            {"units": sale.units,
             "price_per_unit": sale.price_per_unit,
             "total_cost": sale.units * sale.price_per_unit,}
        )
    return sales


def get_units_held_at_date(investment, cut_off_date):
    """
    This gets all the units held for an Investment up to (and including) a certain date.
    """
    purchases = get_purchase_history(investment)
    sales = get_sale_history(investment)

    units_held_at_date = 0
    for purchase_date in list(purchases.keys()):
        if datetime.datetime.strptime(purchase_date, "%d/%m/%Y") <= cut_off_date:
            units_held_at_date += purchases[purchase_date][0][0]
    for sales_date in list(sales.keys()):
        if datetime.datetime.strptime(sales_date, "%d/%m/%Y") <= cut_off_date:
            units_held_at_date -= purchases[purchase_date][0][0]

    return int(units_held_at_date)


# ***********************************************
# **************** Async Scraper ****************
# ***********************************************
@sync_to_async
def get_investment_and_urls():
    """
    Get each Investment and the URL containing the data for that investment. This information can then
    be used to scrape the page and get the values needed.
    """
    investment_and_url = {}
    for investment in list(Investment.objects.all()):
        investment_and_url[investment.symbol] = {
            "investment": investment,
            "url": f"https://bigcharts.marketwatch.com/quotes/multi.asp?view=q&msymb=au:{investment.symbol}+",
        }
    return investment_and_url


async def fetch(session, url):
    """
    Get all the data from the page.
    """
    async with session.get(url) as response:
        return await response.text()


async def scrape(scraper_function):
    """
    Scrape the source for each Investment. Update the the live price for each and create an entry
    into the investment's value history.
    """
    investment_and_url = await get_investment_and_urls()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for value in investment_and_url.values():
            page_data = fetch(session, value["url"])
            tasks.append(asyncio.ensure_future(page_data))
        responses = await asyncio.gather(*tasks)

        for response in responses:
            await scraper_function(investment_and_url, response)


def initiate_async_scape(scraper_function):
    """
    Uses ASX data from BigCharts (MarketWatch) to propagate portfolio with share data.
    There is no official API so data is scraped from their website. Not sure if this
    breaks terms of use.

    This is done asynchronously to improve speed.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(scrape(scraper_function=scraper_function))
