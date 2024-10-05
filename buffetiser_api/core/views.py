from django.shortcuts import render

from core.models import Investment

def get_investment_data():
    return Investment.objects.all()

def get_all_investment_data():
    return Investment.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """