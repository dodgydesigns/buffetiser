import datetime
from http import HTTPStatus
from itertools import count

import schedule

from core.config import Constants
from core.models import DailyChange, Investment, Purchase, Sale
from core.serializers import InvestmentSerializer
from core.services.investment_details import (
    get_all_details_for_investment,
    get_portfolio_totals,
    get_portfolio_value_history,
    scraper_function_get_daily_change,
    scraper_function_investment_and_history,
)
from core.services.investment_helpers import fe_string_to_date, initiate_async_scrape
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from datetime import datetime
import time

# There can be multiple purchases/sales of an Investment in a single day. The records
# only keep date not time so we need to be able to differentiate.
trade_counter = count()


@api_view(["POST"])
def update_daily_changes(request):
    """
    When hit, this endpoint updates the daily change values for ALL Investments.
    As this is just a temporary value that is updated constantly, the previous
    values are of no use and can be deleted.
    """
    # Clear the current data
    DailyChange.objects.all().delete()

    initiate_async_scrape(scraper_function_get_daily_change)

    return HttpResponse(status=204)


@api_view(["POST"])
def update_all_investments(request):
    """
    This updates ALL the data for ALL investments.
    """
    update_daily_changes(request._request)
    initiate_async_scrape(scraper_function_investment_and_history)

    return JsonResponse({}, status=204)


class AllInvestmentsDataView(APIView):
    """
    This is the main endpoint for the front end. It basically gets all the information
    required for the UI to display all the data for each Investment. The History data
    for plots is handled separately.
    """

    def get(self, _):
        all_investment_data = []
        for investment in list(Investment.objects.all()):
            all_investment_data.append(get_all_details_for_investment(investment))

        return JsonResponse({"all_investment_data": all_investment_data}, status=200)


class AllConstantsView(APIView):
    """
    Get all the constants required for adding, buying and selling Investments.
    """

    Constants.InvestmentType.choices

    def get(self, _):
        constants = {
            "type": Constants.InvestmentType.choices,
            "currency": Constants.Currencies.choices,
            "exchange": Constants.Exchanges.choices,
            "platform": Constants.Platforms.choices,
        }

        return JsonResponse(constants, status=200)


class ConfigView(APIView):
    """ """

    def post(self, _):
        print("*" * 60)
        print("*" * 60)
        return JsonResponse(status=200)


class BackupDBView(APIView):
    """ """

    def post(self, _):
        print("*" * 60)
        print("BackupDBView")
        print("*" * 60)
        return JsonResponse({}, status=200)


class CronTimeView(APIView):
    """ """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.run_schedule = True
        self.cron_time = "15:00"
        self.cron_job = schedule.every().day.at("15:00").do(self.share_price_updater)

    def get(self, _):
        print("GET "*60)
        print(self.cron_time)
        return JsonResponse({"cron_time": self.cron_time}, status=200)

    def post(self, response):
        """
        Sets a daily schedule to update the prices for all investments. In case the scheduled time is changed,
        the schedule is cleared and restarted with the new run time.
        """
        self.cron_time = response.data
        self.run_schedule = False
        schedule.clear()
        self.cron_job = schedule.every().day.at(self.cron_time, "Australia/Perth").do(self.share_price_updater)
        self.run_schedule = True
        # Loop so that the scheduling task keeps on running all time.
        while self.run_schedule:
            print(schedule.idle_seconds())
            schedule.run_pending()
            time.sleep(1)

        return JsonResponse({}, status=200)
    
    def share_price_updater(self):
        """
        
        """
        print("RAN " * 60)
        # update_all_investments()


class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer


class PortfolioTotals(APIView):
    """
    Aggregate all the purchases, sales and values by date for the chart and
    the overall totals for the header and history for the chart.
    """

    # TODO: don't forget reinvestment and dividend payouts

    def get(self, _):
        payload = {
            "portfolio_totals": get_portfolio_totals(),
            "portfolio_history": get_portfolio_value_history(),
        }
        return JsonResponse(payload, status=200)


class NewInvestmentView(APIView):
    """
    Create a new Investment object. A Purchase object will necessarily be created at the same time but
    most values will be 0. This allows an Investment to be watched.
    Reply from the front end will be:
    {"symbol":"","name":"","currency":"","exchange":"","platform":"","units":"","pricePerUnit":"","fee":""}
    """

    def post(self, request):
        new_investment_data = request.data

        try:
            if not new_investment_data["symbol"] in [
                inv.symbol for inv in Investment.objects.all()
            ]:
                new_investment = Investment.objects.create(
                    key=new_investment_data["symbol"],
                    name=new_investment_data["name"],
                    symbol=new_investment_data["symbol"],
                )
                new_investment.live_price = get_all_details_for_investment(
                    new_investment
                )["last_price"]
                new_investment.live_price

                purchase, created = Purchase.objects.get_or_create(
                    investment=new_investment,
                    units=0,
                    price_per_unit=new_investment.live_price[0],
                    fee=0,
                    date=datetime.datetime.now(),
                    trade_count=next(trade_counter),
                )
                if created:
                    purchase.save()
        except Exception as e:
            print("*" * 60)
            print(e)
            print("*" * 60)

        return HttpResponse(HTTPStatus.OK)


class PurchaseView(APIView):
    """
    Create a purchase entry for an existing Investment.
    Reply from the front end will be:
        'symbol', 'currency', 'exchange', 'platform', 'units', 'pricePerUnit', 'fee', 'date'
    """

    def post(self, request):
        purchase_data = request.data
        purchase_investment = Investment.objects.filter(
            symbol=purchase_data["symbol"]
        ).first()

        try:
            purchase, created = Purchase.objects.get_or_create(
                investment=purchase_investment,
                units=float(purchase_data["units"]),
                price_per_unit=float(purchase_data["pricePerUnit"]),
                fee=purchase_data["fee"],
                date=fe_string_to_date(purchase_data["date"]),
                trade_count=next(trade_counter),
            )
            if created:
                purchase.save()
        except Exception as e:
            print("*" * 60)
            print(e)
            print("*" * 60)

        return HttpResponse(HTTPStatus.OK)


class SaleView(APIView):
    """
    Create a sal entry for an existing Investment.
    Reply from the front end will be:
        'symbol', 'currency', 'exchange', 'platform', 'units', 'pricePerUnit', 'fee', 'date'
    """

    def post(self, request):
        sale_data = request.data
        sale_investment = Investment.objects.filter(symbol=sale_data["symbol"]).first()

        try:
            sale, created = Sale.objects.get_or_create(
                investment=sale_investment,
                units=float(sale_data["units"]),
                price_per_unit=float(sale_data["pricePerUnit"]),
                fee=sale_data["fee"],
                date=fe_string_to_date(sale_data["date"]),
                trade_count=next(trade_counter),
            )
            if created:
                sale.save()
        except Exception as e:
            print("*" * 60)
            print(e)
            print("*" * 60)

        return HttpResponse(HTTPStatus.OK)


class RemoveView(APIView):
    """
    Create a sal entry for an existing Investment.

    """

    def post(self, request):
        print("*" * 60)
        print("DELETE")
        print("*" * 60)
        # sale_data = request.data
        # sale_investment = Investment.objects.filter(symbol=sale_data["symbol"]).first()

        # try:
        #     sale, created = Sale.objects.get_or_create(
        #         investment=sale_investment,
        #         units=float(sale_data["units"]),
        #         price_per_unit=float(sale_data["pricePerUnit"]),
        #         fee=sale_data["fee"],
        #         date=fe_string_to_date(sale_data["date"]),
        #         trade_count=next(trade_counter),
        #     )
        #     if created:
        #         sale.save()
        # except Exception as e:
        #     print("*"*60)
        #     print(e)
        #     print("*"*60)

        return HttpResponse(HTTPStatus.OK)
