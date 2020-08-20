from django.contrib import admin

from .models import (
    Address,
    Currency,
    Language,
    HashTag,
)


class CurrencyAdmin(admin.ModelAdmin):
    readonly_fields = (
        'slug',
    )


class LanguageAdmin(admin.ModelAdmin):
    readonly_fields = (
        'slug',
    )


admin.site.register(Address)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(HashTag)
