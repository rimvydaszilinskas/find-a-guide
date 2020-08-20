from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin

from .models import User, Profile


class APIToken(Token):
    class Meta:
        proxy = True
        verbose_name = 'API Token'
        verbose_name_plural = 'API Tokens'


class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    readonly_fields = (
        'uuid',
        'verification_string',
        'email',
    )

    fieldsets = (
        (None, {
            "fields": (
                'username',
                'password',
                'uuid',
            ),
        }), ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'timezone',
                'verification_string',
                'currency',
            )
        }), ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }), ('Dates', {
            'fields': (
                'last_login',
                'date_joined',
            )
        })
    )

    def get_readonly_fields(self, request, obj=None):
        fields = super(self.__class__, self).get_readonly_fields(
            request, obj=obj)

        if obj is None:
            return ('uuid', 'verification_string')
        return fields


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = (
        'user',
    )


admin.site.unregister(Token)
admin.site.register(APIToken, TokenAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
