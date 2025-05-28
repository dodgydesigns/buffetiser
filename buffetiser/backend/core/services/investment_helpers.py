import asyncio
import datetime

import aiohttp
from asgiref.sync import sync_to_async

from core.models import Investment, Sale


def date_to_string(date):
    """Ensure all dates are formatted the same."""
    return date.strftime("%d/%m/%Y")


def date_to_datetime(date):
    """Ensure all dates are formatted the same."""
    return datetime.datetime(date.year, date.month, date.day)


def string_to_date(date_string):
    """Ensure all dates are formatted the same."""
    return datetime.datetime.strptime(date_string, "%d/%m/%Y")


def fe_string_to_date(date_string):
    """Date string coming from the front end."""
    date_string = date_string.split("T")[0]
    return datetime.datetime.strptime(date_string, "%Y-%m-%d")


def nearest(items, pivot):
    """
    Find the nearest item (date) in a list.
    """
    return min(items, key=lambda x: abs(x - pivot.date()))


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


def initiate_async_scrape(scraper_function):
    """
    Uses ASX data from BigCharts (MarketWatch) to propagate portfolio with share data.
    There is no official API so data is scraped from their website. Not sure if this
    breaks terms of use.

    This is done asynchronously to improve speed.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(scrape(scraper_function=scraper_function))
