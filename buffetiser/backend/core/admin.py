from core.models import (
    DailyChange,
    DividendPayment,
    DividendReinvestment,
    History,
    Investment,
    Purchase,
    Sale,
)
from django.contrib import admin

# Register your models here.
admin.site.register(Investment)
admin.site.register(Purchase)
admin.site.register(Sale)
admin.site.register(DividendReinvestment)
admin.site.register(DividendPayment)
admin.site.register(History)
admin.site.register(DailyChange)
