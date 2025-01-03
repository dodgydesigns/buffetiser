from core.config import Constants
from core.models import DailyChange, Investment, Purchase
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
from http import HTTPStatus


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

    return HttpResponse(status=204)


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
        payload = {"portfolio_totals": get_portfolio_totals(), 
                   "portfolio_history": get_portfolio_value_history(),}
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

        print("*"*60)
        print(new_investment_data["symbol"])
        print("*"*60)
        # print(Investment.objects.get(symbol=new_investment_data["symbol"]))
        # print("*"*60)
        # print(get_all_details_for_investment(Investment.objects.get(symbol=new_investment_data["symbol"])))

        # try:
        #     print("*1"*60)
        #     if not new_investment_data["symbol"] in [inv.symbol for inv in Investment.objects.all()]:
        #         new_investment = Investment.objects.create(key=new_investment_data["symbol"],
        #                                                 name=new_investment_data["name"],
        #                                                 symbol=new_investment_data["symbol"],
        #                                             )
        #         print("*"*60)
        #         # print(get_all_details_for_investment(new_investment))
        #         new_investment.live_price = get_all_details_for_investment(new_investment)["last_price"]
        #         new_investment.live_price
        #         print("*"*60)
        #         # new_investment.save()

                

        #         purchase, created = Purchase.objects.get_or_create(
        #             investment=new_investment,
        #             units=0,
        #             price_per_unit=new_investment.live_price[0],
        #             fee=0,
        #             date=datetime.datetime.now(),
        #             trade_count=0,
        #         )
        #         if created:
        #             purchase.save()
        # except Exception as e:
        #     print("*"*60)
        #     print(e)
        #     print("*"*60)

        return HttpResponse(HTTPStatus.OK)
    
class PurchaseView(APIView):
    """
    Create a new Investment object. A Purchase object will necessarily be created at the same time but 
    most values will be 0. This allows an Investment to be watched.
    Reply from the front end will be:
        'symbol': 'VAS', 'currency': 'AUD', 'exchange': 'XASX', 'platform': 'CMC', 
        'units': '49', 'pricePerUnit': '100.9050', 'fee': '11', 'date': '2024-12-23T09:29:49.000Z'
    """

    def post(self, request):
        purchase_data = request.data
        purchase_investment = Investment.objects.filter(symbol=purchase_data["symbol"]).first()

        try:
            purchase, created = Purchase.objects.get_or_create(
                investment=purchase_investment,
                units=float(purchase_data["units"]),
                price_per_unit=float(purchase_data["pricePerUnit"]),
                fee=purchase_data["fee"],
                date=fe_string_to_date(purchase_data["date"]),
                trade_count=1,
            )
            if created:
                purchase.save()
        except Exception as e:
            print("*"*60)
            print(e)
            print("*"*60)

        return HttpResponse(HTTPStatus.OK)
    

class SaleView(APIView):
    """
    Create a new Investment object. A Purchase object will necessarily be created at the same time but 
    most values will be 0. This allows an Investment to be watched.
    Reply from the front end will be:
    {"symbol":"","name":"","currency":"","exchange":"","platform":"","units":"","pricePerUnit":"","fee":""}
    """

    def post(self, request):
        purchase = request.data

        print("*"*60)
        print(purchase["symbol"])