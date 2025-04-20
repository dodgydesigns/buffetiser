import datetime
import subprocess
import time
from datetime import datetime
from http import HTTPStatus
from itertools import count
from threading import Thread
import schedule

from core.config import Constants
from core.models import (Configuration, DailyChange, DividendPayment,
                         DividendReinvestment, Investment, Purchase, Sale)
from core.serializers import InvestmentSerializer
from core.services.investment_details import (
    get_all_details_for_investment, get_portfolio_totals,
    get_portfolio_value_history, scraper_function_get_daily_change,
    scraper_function_investment_and_history)
from core.services.investment_helpers import (fe_string_to_date,
                                              initiate_async_scrape)
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

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
        return JsonResponse(status=200)

    def post(self, _):
        return JsonResponse(status=200)


class BackupDBView(APIView):
    """ """

    def post(self, _):
        print("*" * 60)
        print("BackupDBView")
        print("*" * 60)

        # Database credentials
        DB_NAME = "buffetiser"
        DB_USER = "buffetiser"
        DB_PASSWORD = "password"
        DB_HOST = "localhost"  # Change if your DB is hosted remotely
        DB_PORT = "5432"
        BACKUP_DIR = "~/Downloads/db_bk/"

        # Generate backup file name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_file = f"{BACKUP_DIR}backup_{timestamp}.sql"

        # Command to dump the database
        psql_bin = (
            "export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/16/bin"
        )
        dump_cmd = f"pg_dump -U {DB_USER} -h {DB_HOST} -p {DB_PORT} -d {DB_NAME} -F c -f {backup_file}"
        print("*" * 60)
        print(psql_bin)
        print(dump_cmd)
        print("*" * 60)
        try:
            subprocess.run(psql_bin, shell=True, check=True)
            subprocess.run(
                dump_cmd, shell=True, check=True, env={"PGPASSWORD": DB_PASSWORD}
            )
            print(f"Backup successful: {backup_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error during backup: {e}")

        return JsonResponse({}, status=200)


class RestoreDBView(APIView):
    """ """

    def post(self, _):
        print("*" * 60)
        print("RestoreDBView")
        print("*" * 60)

    # Database credentials
    DB_NAME = "your_db_name"
    DB_USER = "your_db_user"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    BACKUP_FILE = "/path/to/backup/directory/backup_xxxxxx.sql"  # Replace with actual backup filename

    # Command to restore the database
    restore_cmd = f"pg_restore -U {DB_USER} -h {DB_HOST} -p {DB_PORT} -d {DB_NAME} -c {BACKUP_FILE}"

    try:
        subprocess.run(
            restore_cmd, shell=True, check=True, env={"PGPASSWORD": "your_db_password"}
        )
        print(f"Database restored from {BACKUP_FILE}")
    except subprocess.CalledProcessError as e:
        print(f"Error during restoration: {e}")


class CronTimeView(APIView):
    """
    Controls a CRON like thread that updates all share prices at a certain time each day.
    It wont update on weekends - save the price server some traffic :)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.countdown = CountdownTask()

    def get(self, _):
        if len(Configuration.objects.all()) == 0:
            config = Configuration()
            config.save()

        return JsonResponse(
            {"cron_time": Configuration.objects.all().first().update_time}, status=200
        )

    def post(self, response):
        """
        Sets a daily schedule to update the prices for all investments. In case the scheduled time is changed,
        the schedule is cleared and restarted with the new run time.
        """
        config = Configuration.objects.all().first()
        config.update_time = response.data
        config.save()

        if self.countdown.running():
            self.countdown.terminate()
        self.countdown.setup(
            Configuration.objects.all().first().update_time,
            Configuration.objects.all().first().update_time_zone,
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

    # from django.db.models.signals import post_save, post_delete
    # from django.dispatch import receiver
    # from myapp.models import ExpensiveModel
    # from django.core.cache import cache

    # @receiver([post_save, post_delete], sender=ExpensiveModel)
    # def clear_expensive_cache(sender, **kwargs):
    # cache.delete('expensive_query_result')
    
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
            all_transactions.sort(key=lambda x: x.get("date") or x.get("payment_date") or x.get("reinvestment_date"))

            report_dict[investment.key] = {
                "key": investment.key,
                "name": investment.name,
                "symbol": investment.symbol,
                "transactions": all_transactions,
            }

        # Return the report data as JSON
        return JsonResponse(report_dict, status=200)


class RemoveView(APIView):
    """

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


# class DividendPaymentView(APIView):
#     """
#     Create a dividend payment entry for an existing Investment.
#     Reply from the front end will be:
#         'symbol', 'currency', 'exchange', 'platform', 'units', 'pricePerUnit', 'fee', 'date'
#     """
#     def post(self, request):
#         dividend_data = request.data
#         dividend_investment = Investment.objects.filter(symbol=dividend_data["symbol"]).first()
#
#         try:
#             dividend, created = DividendPayment.objects.get_or_create(                    
#                 investment=dividend_investment,
#                 units=float(dividend_data["units"]),
#                 price_per_unit=float(dividend_data["pricePerUnit"]),
#                 fee=dividend_data["fee"],
#                 date=fe_string_to_date(dividend_data["date"]),
#                 trade_count=next(trade_counter),
#             )
#             if created:
#                 dividend.save()
#         except Exception as e:
#             print("*" * 60)
#             print(e)
#             print("*" * 60)
#         return HttpResponse(HTTPStatus.OK)


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
            reinvestment_date=fe_string_to_date(reinvestment_data["date"]),
        )
        reinvestment.save()
        
        return HttpResponse(HTTPStatus.OK)