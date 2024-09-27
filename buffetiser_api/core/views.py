from django.shortcuts import render

from core.models import Investment

def get_investments():
    return Investment.objects.all()