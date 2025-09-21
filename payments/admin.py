from django.contrib import admin
from .models import FeeType, PaymentSession, PaymentRecord, PricingRule


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


@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'rule_type',
        'min_total_amount',
        'max_total_amount',
        'min_fee_count',
        'max_fee_count',
        'value',
        'is_active',
        'created_at',
    )
    list_filter = ('rule_type', 'is_active', 'created_at')
    search_fields = ('description',)
    ordering = ('min_total_amount', 'min_fee_count')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        (None, {
            'fields': (
                'rule_type',
                'value',
                'description',
                'is_active',
            ),
        }),
        ('Conditions', {
            'fields': (
                'min_total_amount',
                'max_total_amount',
                'min_fee_count',
                'max_fee_count',
            ),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )
