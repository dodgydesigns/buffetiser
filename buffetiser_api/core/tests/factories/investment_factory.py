# import datetime
# import string
# from factory.fuzzy import FuzzyInteger, FuzzyFloat, FuzzyText, FuzzyDate
# from factory import django, SubFactory
# from core.models import Investment, Purchase
# from config.constants import Constants


# class PurchaseFactory(django.DjangoModelFactory):
#     class Meta:
#         model = Purchase

#     investment_name = FuzzyText(length=12, chars=string.ascii_letters, prefix="").fuzz()
#     exchange = Constants.Exchanges.XASX
#     symbol = FuzzyText(length=3, chars=string.ascii_letters, prefix="").fuzz()

#     units = FuzzyInteger(1, 1000).fuzz()
#     price_per_unit = FuzzyFloat(0.1, 100).fuzz()
#     fee = FuzzyInteger(1, 20).fuzz()

#     investment = Investment.objects.get_or_create(
#         key=f"{exchange}:{symbol}", price_history={}, value_history={}
#     )[0]
#     print(investment)
#     # investment.price_history[str(datetime.date.today())] = price_per_unit
#     # investment.value_history[str(datetime.date.today())] = price_per_unit * units
