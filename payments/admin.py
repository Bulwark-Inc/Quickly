from django.contrib import admin
from .models import FeeType, PaymentSession, PaymentRecord


@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'charge', 'total', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    readonly_fields = ('total',)
    fieldsets = (
        (None, {
            'fields': ('name', 'amount', 'charge', 'total', 'description', 'is_active')
        }),
    )


@admin.register(PaymentSession)
class PaymentSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'payment_method', 'total_amount', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('session_id', 'user__email')


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'fee_type', 'amount_paid', 'charge', 'total_amount', 'status', 'date_paid')
    list_filter = ('status', 'date_paid', 'fee_type')
    search_fields = ('user__email', 'fee_type__name')
    readonly_fields = ('total_amount', 'date_paid')

    fieldsets = (
        (None, {
            'fields': ('user', 'fee_type', 'amount_paid', 'charge', 'total_amount', 'session', 'proof_of_payment', 'status', 'date_paid')
        }),
    )
