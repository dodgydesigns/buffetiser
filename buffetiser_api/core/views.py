import json

from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from core.models import DailyChange, Investment
from core.serializers import InvestmentSerializer
from core.services.investment_details import (
    get_all_details_for_investment, scraper_function_get_daily_change,
    scraper_function_investment_and_history)
from core.services.investment_helpers import initiate_async_scape


@api_view(["POST"])
def update_daily_changes(request):
    """
    When hit, this endpoint updates the daily change values for ALL Investments.
    As this is just a temporary value that is updated constantly, the previous
    values are of no use and can be deleted.
    """
    # Clear the current data
    DailyChange.objects.all().delete()

    initiate_async_scape(scraper_function_get_daily_change)

    return HttpResponse(status=204)


@api_view(["POST"])
def update_all_investments(request):
    """
    This updates ALL the data for ALL investments.
    """
    update_daily_changes(request._request)
    initiate_async_scape(scraper_function_investment_and_history)

    return HttpResponse(status=204)


class AllInvestmentsDataView(APIView):
    """
    This is the main endpoint for the front end. It basically gets all the information
    required for the UI to display all the data for each Investment. The History data
    for plots is handled separately.
    """

    def get(self, request):
        all_investment_data = []
        for investment in list(Investment.objects.all()):
            all_investment_data.append(get_all_details_for_investment(investment))

        return JsonResponse({"all_investment_data": all_investment_data}, status=200)


class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
