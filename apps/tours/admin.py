from django.contrib import admin

from .models import (
    TourType,
    Tour,
    Attendee,
    PersonalTour,
)


class TourAdmin(admin.ModelAdmin):
    readonly_fields = (
        'uuid',
    )

    raw_id_fields = (
        'guide',
        'meeting_point',
    )


class TourTypeAdmin(admin.ModelAdmin):
    readonly_fields = (
        'slug',
        'uuid',
    )


admin.site.register(TourType, TourTypeAdmin)
admin.site.register(Tour, TourAdmin)
admin.site.register(Attendee)
admin.site.register(PersonalTour)
