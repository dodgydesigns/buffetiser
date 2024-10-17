import json

from core.models import DailyChange, Investment
from core.serializers import InvestmentSerializer
from core.services.investment_details import (
    get_all_details_for_investment, scraper_function_get_daily_change,
    scraper_function_investment_and_history)
from core.services.investment_helpers import initiate_async_scape
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView

# def update_daily_changes(request):
#     """ """
#     # Clear the current data
#     DailyChange.objects.all().delete()

#     initiate_async_scape(scraper_function_get_daily_change)

#     return HttpResponse("FART", status=204)


# def update_all_investments(request):
#     """ """
#     initiate_async_scape(scraper_function_investment_and_history)
#     initiate_async_scape(scraper_function_get_daily_change)

#     return HttpResponse(request, status=204)


class AllInvestmentsDataView(APIView):
    def get(self, request):
        all_investment_data = []
        for investment in list(Investment.objects.all()):
            all_investment_data.append(get_all_details_for_investment(investment))

        return JsonResponse({"data": all_investment_data}, status=200)


class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
