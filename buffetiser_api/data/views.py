from django.http import HttpResponse

from core.models import Investment, Purchase
from data.models import History


def update_all_investment_history(request):
    text = "<h1>Buffetiser Unchained Data!</h1>"

    p1 = Purchase()
    p1.symbol = "MP1"
    p1.investment_name = "MegaPort"
    p1.units = 50
    p1.price_per_unit = 1
    p1.fee = 10
    p1.save()

    p2 = Purchase()
    p2.symbol = "CAT"
    p2.investment_name = "Catapault"
    p2.units = 500
    p2.price_per_unit = 20
    p2.fee = 10
    p2.save()

    investments = Investment.objects.all()
    for investment in investments:
        history = History.objects.get(investment=investment)
        history.update_history()
        history.print_stuff()

    return HttpResponse(text)
