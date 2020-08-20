from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import (
    TourGuideProfile,
    TourGuideRating,
    PersonalGuideRequest,
)


class TourGuidProfileAdmin(OSMGeoAdmin):
    raw_id_fields = (
        'user',
    )

    readonly_fields = (
        'uuid',
    )

    list_display = (
        '__str__',
        'active',
        'rating',
        'is_free',
        'price',
    )

    fieldsets = (
        (None, {
            'fields': (
                'uuid',
                'user',
                'active',
                'approved',
            ),
        }), ('Details', {
            'fields': (
                'tour_types',
                'languages',
                'price',
                'intro',
            )
        }), ('Location', {
            'fields': (
                'country',
                'town',
                'point',
            )
        })
    )


class TourGuideRatingAdmin(admin.ModelAdmin):
    pass


class PersonalGuideRequestAdmin(admin.ModelAdmin):
    pass


admin.site.register(TourGuideProfile, TourGuidProfileAdmin)
admin.site.register(TourGuideRating, TourGuideRatingAdmin)
admin.site.register(PersonalGuideRequest, PersonalGuideRequestAdmin)
