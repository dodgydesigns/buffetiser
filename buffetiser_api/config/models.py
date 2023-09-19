from django.db.models import Model, CharField


class UserSettings(Model):

    # user = CharField(primay_key=True)

    # hours_between_live_updates = IntegerField(defalut=24)
    shares_data_source = CharField(max_length=64)
    crypto_data_source = CharField(max_length=64)
    default_currency = CharField(max_length=64)
    default_shares_exchange = CharField(max_length=64)
    default_shares_platform = CharField(max_length=64)
    default_crypto_exchange = CharField(max_length=64)
    default_crypto_platform = CharField(max_length=64)
