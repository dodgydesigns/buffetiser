import datetime
import subprocess
import time
from datetime import datetime
from http import HTTPStatus
from itertools import count
from threading import Thread

import schedule
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from core.config import Constants
from core.models import (Configuration, DailyChange, DividendPayment,
                         DividendReinvestment, Investment, Purchase, Sale)
from core.serializers import InvestmentSerializer
from core.services.investment_details import (get_all_details_for_investment,
                                              get_portfolio_totals,
                                              get_portfolio_value_history)
from core.services.investment_helpers import (fe_string_to_date,
                                              initiate_async_scrape)
from core.services.investment_updaters import (
    scraper_function_get_daily_change, scraper_function_investment_and_history)

# There can be multiple purchases/sales of an Investment in a single day. The records
# only keep date not time so we need to be able to differentiate.
trade_counter = count()


@api_view(["POST"])
def update_daily_changes():
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
    update_daily_changes()
    initiate_async_scrape(scraper_function_investment_and_history)
    print("Updated all investments prices")

    # Clear the cache to ensure fresh data is served
    cache_key = 'expensive_query_result'
    if cache.get(cache_key) is not None:
        cache.delete(cache_key)

    # Trigger a backup of the database after updating
    BackupDBView().post(request)

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
    """Nothing to be done here at this point."""

    def get(self, _):
        return JsonResponse({}, status=200)

    def post(self, _):
        return JsonResponse({}, status=200)


class BackupDBView(APIView):
    """ Create a backup of the database by dumping it to a JSON file in the fixtures directory."""

    def post(self, _):
        # Generate backup file name with timestamp
        BACKUP_DIR = "fixtures/"
        timestamp = datetime.now().strftime("%y-%m-%d")
        backup_file = f"{BACKUP_DIR}buffetiser_{timestamp}_data.json"

        # Command to dump the data
        dump_cmd = f"python manage.py dumpdata \
                     --exclude contenttypes \
                     --exclude auth.permission \
                     --exclude sessions \
                     --indent 2 > {backup_file}"

        try:
            subprocess.run(dump_cmd, shell=True, check=True)
            print(f"Backup successful: {backup_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error during backup: {e}")

        return JsonResponse({}, status=200)


class RestoreDBView(APIView):
    """ Allows the user to restore the database from a backup file contained in the fixtures directory."""

    def post(self, _, path):
        print("*" * 60)
        print(f"...{path}...")
        print("*" * 60)
        # Generate backup file name with timestamp
        BACKUP_DIR = "fixtures/"

        # Command to dump the data
        dump_cmd = f"python manage.py loaddata \
                     fixtures/{path}"
        try:
            subprocess.run(dump_cmd, shell=True, check=True)
            print(f"Backup successful: {path}")
        except subprocess.CalledProcessError as e:
            print(f"Error during backup: {e}")

        return JsonResponse({}, status=200)


class CronTimeView(APIView):
    """
    Controls a CRON like thread that updates all share prices at a certain time each day.
    It wont update on weekends - save the price server some traffic :)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.countdown = CountdownTask()
        self.config: Configuration = Configuration.objects.all().first() or Configuration()

    def get(self, _):
        return JsonResponse(
            {"cron_time": self.config.update_time}, status=200
        )

    def post(self, response):
        """
        Sets a daily schedule to update the prices for all investments. In case the scheduled time is changed,
        the schedule is cleared and restarted with the new run time.
        """

        self.config.update_time = response.data
        self.config.save()

        if self.countdown.running():
            self.countdown.terminate()
        self.countdown.setup(
            self.config.update_time,
            self.config.update_time_zone,
        )
        countdown_thread = Thread(target=self.countdown.run)
        countdown_thread.setDaemon(True)
        countdown_thread.start()

        return JsonResponse({}, status=200)


class CountdownTask:
    """
    This creates a threaded task that can be interrupted, updated and restarted.
    """

    def __init__(self):
        self._running = True

    def running(self):
        return self._running

    def terminate(self):
        schedule.clear()
        self._running = False

    def setup(self, time, timezone):
        schedule.every().day.at(time, timezone).do(self.share_price_updater)
        # schedule.every(1).minutes.do(self.share_price_updater)
        self._running = True

    def share_price_updater(self):
        day_number = datetime.today().weekday()
        if day_number < 5:
            print("RAN " * 60)
            # update_daily_changes()
            initiate_async_scrape(scraper_function_investment_and_history)
            print("Updated all investments prices")
        else:
            print("Weekend. Not running updates")

    def run(self):
        """Loop so that the scheduling task keeps on running all time."""
        while self._running:
            print(f"{schedule.idle_seconds()}")
            schedule.run_pending()
            time.sleep(1)


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
        cache_key = 'expensive_query_result'
        payload = cache.get(cache_key)

        if payload is None:
            payload = {
                "portfolio_totals": get_portfolio_totals(),
                "portfolio_history": get_portfolio_value_history(),
            }
            cache.set(cache_key, payload, timeout=300)  # Cache for 5 minutes


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
                new_investment.live_price = get_all_details_for_investment(new_investment)["last_price"]
                new_investment.save()

                purchase, created = Purchase.objects.get_or_create(
                    investment=new_investment,
                    units=0,
                    price_per_unit=new_investment.live_price,
                    fee=0,
                    date=datetime.now(),
                    trade_count=next(trade_counter),
                    currency = new_investment_data["currency"],
                    exchange = new_investment_data["exchange"],
                    platform = new_investment_data["platform"],
                    visible = True,
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


class ReportsView(APIView):
    """
    Get all the details of each investment for a comprehensive report.
    """
    def get(self, _):

        report_dict = {}
        for investment in Investment.objects.all():
            purchases = [p.to_json() | {"type": "purchase"} for p in Purchase.objects.filter(investment=investment)]
            sales = [s.to_json() | {"type": "sale"} for s in Sale.objects.filter(investment=investment)]
            dividends = [d.to_json() | {"type": "dividend"} for d in DividendPayment.objects.filter(investment=investment)]
            reinvestments = [r.to_json() | {"type": "reinvestment"} for r in DividendReinvestment.objects.filter(investment=investment)]

            # Combine all and sort by date
            all_transactions = purchases + sales + dividends + reinvestments
            all_transactions.sort(key=lambda x: x.get("date") or "")

            report_dict[investment.key] = {
                "key": investment.key,
                "name": investment.name,
                "symbol": investment.symbol,
                "transactions": all_transactions,
            }

        return JsonResponse(report_dict, status=200)


class RemoveView(APIView):
    """
    Hide an Investment from the font end.
    """

    def post(self, request):
        remove_investment = Investment.objects.get(symbol=request.data["symbol"])
        remove_investment.visible = False
        remove_investment.save()

        return HttpResponse(HTTPStatus.OK)


class LogoutAndBlacklistRefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=400)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=200)
        except AttributeError:
            return Response({"error": "Token blacklisting is not enabled. Ensure 'rest_framework_simplejwt.token_blacklist' is in INSTALLED_APPS."}, status=500)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=400)


class DividendPaymentView(APIView):
    """
    Create a dividend payment entry for an existing Investment.
    Reply from the front end will be:
        'symbol', 'currency', 'exchange', 'platform', 'units', 'pricePerUnit', 'fee', 'date'
    """
    def post(self, request):
        dividend_data = request.data
        dividend_investment = Investment.objects.filter(symbol=dividend_data["symbol"]).first()
        dividend= DividendPayment.objects.create(                    
            investment=dividend_investment,
            value=float(dividend_data["amount"]),
            date=fe_string_to_date(dividend_data["date"]))
        dividend.save()

        return HttpResponse(HTTPStatus.OK)


class DividendReinvestmentView(APIView):
    """
    Create a dividend reinvestment entry for an existing Investment.
    Reply from the front end will be:
        'symbol', 'currency', 'exchange', 'platform', 'units', 'pricePerUnit', 'fee', 'date'
    """
    def post(self, request):
        reinvestment_data = request.data
        reinvestment_investment = Investment.objects.filter(symbol=reinvestment_data["symbol"]).first()

        reinvestment = DividendReinvestment.objects.create(                    
            investment=reinvestment_investment,
            units=float(reinvestment_data["units"]),
            date=fe_string_to_date(reinvestment_data["date"]),
        )
        reinvestment.save()
        
        return HttpResponse(HTTPStatus.OK)