# from django.http import HttpResponse
# from config.constants import Constants

# from core.models import Investment, Purchase, Sale
# from data.models import History


# def create_test_data(request):
#     text = "<h1>Buffetiser Unchained Data!</h1>"

#     print("test_purchase")

#     p1 = Purchase()
#     p1.symbol = "MP1"
#     p1.investment_name = "MegaPort"
#     p1.units = 50
#     p1.price_per_unit = 1
#     p1.fee = 10
#     p1.save()

#     p2 = Purchase()
#     p2.symbol = "CAT"
#     p2.investment_name = "Catapault"
#     p2.units = 500
#     p2.price_per_unit = 20
#     p2.fee = 10
#     p2.save()

#     p3 = Purchase()
#     p3.symbol = "MP1"
#     p3.investment_name = "MegaPort"
#     p3.units = 50
#     p3.price_per_unit = 1
#     p3.fee = 10
#     p3.save()

#     key = Investment.generate_key(exchange=Constants.Exchanges.XASX, symbol="MP1")
#     investment = Investment.objects.filter(key=key).first()
#     s1 = Sale(investment=investment)
#     s1.units = 100
#     s1.price_per_unit = 2
#     s1.fee = 0
#     s1.save()

#     for investment in Investment.objects.all():
#         print(f"{investment.name} ({investment.symbol})")
#         print(f"price_history {investment.price_history}")
#         print(f"value_history {investment.value_history}")
#         print(f"total_cost {investment.total_cost_excluding_fees}")
#         print(f"total_fees {investment.total_fees}")
#         print(f"total_profit {investment.total_profit}")
#         print(f"total_units {investment.total_units}")
#         print("\n")

#     investments = Investment.objects.all()
#     for investment in investments:
#         history = History.objects.get(investment=investment)
#         history.update_history()
#         history.print_stuff()

#     return HttpResponse(text)
