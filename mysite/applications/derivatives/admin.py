from django.contrib import admin
from .models import EconomicIndicatorStandard
from .models import EconomicIndicatorCounterparty

# Register your models here.
admin.site.register(EconomicIndicatorStandard)
admin.site.register(EconomicIndicatorCounterparty)
