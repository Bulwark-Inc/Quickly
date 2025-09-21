from django.contrib import admin
from .models import Feature, AboutBullet, OverviewStep, Testimonial, PricingOption, PricingOption


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'text')
    search_fields = ('title', 'text', 'icon')


@admin.register(AboutBullet)
class AboutBulletAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'text')
    search_fields = ('title', 'text', 'icon')


@admin.register(OverviewStep)
class OverviewStepAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'icon', 'desc')
    list_editable = ('order',)
    list_display_links = ('title',)  # <-- Added this line to fix the error
    search_fields = ('title', 'desc', 'icon')
    ordering = ('order',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'quote')
    search_fields = ('name', 'role', 'quote')


@admin.register(PricingOption)
class PricingOptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'headline', 'description', 'cta_text')
    search_fields = ('title', 'headline', 'description', 'features', 'cta_text')
