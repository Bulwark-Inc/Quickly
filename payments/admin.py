from django.contrib import admin
from .models import FeeType, PaymentRecord

admin.site.register(FeeType)
admin.site.register(PaymentRecord)
