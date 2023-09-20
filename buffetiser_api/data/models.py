# from datetime import datetime, timedelta
# from django.utils import timezone
# import requests
# from bs4 import BeautifulSoup

# from django.db.models import (
#     Model,
#     FloatField,
#     IntegerField,
#     DateTimeField,
#     ForeignKey,
#     CASCADE,
# )

# from core.models import Investment


# class History(Model):
#     """
#     This will hold a lot of data about the performance of an
#     Investment for each day. It will be used to supplement the portfolio
#     buy/sell data.
#     """

#     investment = ForeignKey(to=Investment, on_delete=CASCADE)
#     date = DateTimeField(auto_now=True)
#     open = FloatField(default=0)
#     high = FloatField(default=0)
#     low = FloatField(default=0)
#     close = FloatField(default=0)
#     adjustedClose = FloatField(default=0)
#     volume = IntegerField(default=0)

#     def update_history(self):
#         """ """
#         if timezone.now() - self.date >= timedelta(days=1):
#             print("ggooooooooood")
#         else:
#             print("baaaaaad")
#         # self.use_big_charts()
#         # self.save()

#     def use_big_charts(self):
#         """
#         Uses ASX data from BigCharts (MarketWatch) to propagate portfolio with share data.
#         There is no official API so data is scraped from their website. Not sure if this
#         breaks terms of use.
#         :param symbol: The investment symbol to fetch data for.
#         :param todayString: The date for today.
#         """

#         url = "https://bigcharts.marketwatch.com/quotes/multi.asp?view=q&msymb=" + \
#               "au:{}+".format(self.investment.symbol)
#         page = requests.get(url)
#         soup = BeautifulSoup(page.content, "html.parser")
#         last_price = soup.find("td", {"class": "last-col"}).text
#         high = soup.find("td", {"class": "high-col"}).text
#         low = soup.find("td", {"class": "low-col"}).text
#         volume = soup.find("td", {"class": "volume-col"}).text

#         self.date = datetime.now()
#         self.open = float(low)
#         self.high = float(high)
#         self.low = float(low)
#         self.close = float(last_price)
#         self.adjustedClose = float(last_price)
#         self.volume = int(volume.replace(",", ""))

#     def print_stuff(self):

#         print(self.investment.name)
#         print(f"date: {self.date}")
#         print(f"open: {self.open}")
#         print(f"high: {self.high}")
#         print(f"low: {self.low}")
#         print(f"close: {self.close}")
#         print(f"adjusted: {self.adjustedClose}")
#         print(f"volume: {self.volume}")
#         print("\n")
