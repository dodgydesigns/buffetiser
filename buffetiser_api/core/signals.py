from django.dispatch import receiver
from core.models import Investment, Purchase, Sale
from django.db.models.signals import pre_save

from data.models import History


@receiver(pre_save, sender=Purchase)
def create_purchase(sender, instance, **kwargs):
    print("---------------create_purchase--------------------")

    key = Investment.generate_key(exchange=instance.exchange, symbol=instance.symbol)
    investment_response = Investment.objects.get_or_create(key=key)
    investment = investment_response[0]
    if investment_response[1]:
        investment.price_history = {}
        investment.value_history = {}
        investment.name = instance.investment_name
        investment.symbol = instance.symbol

    investment.add_purchase(purchase=instance)
    history_response = History.objects.get_or_create(investment=investment)
    history = history_response[0]
    if history_response[1]:
        pass  # no special setup needed
    history.update_history()
    instance.investment = investment


@receiver(pre_save, sender=Sale)
def create_sale(sender, instance, **kwargs):
    print("---------------create_sale--------------------")

    investment = instance.investment
    if investment is None:
        raise Exception("No such Investment exists.")
    investment.add_sale(sale=instance)
