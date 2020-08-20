from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from apps.utils.models import BaseModel


class TourType(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=50, db_index=True,
                            unique=True, primary_key=True)

    def __str__(self):
        return self.name


class Tour(BaseModel):
    name = models.CharField(max_length=30)

    type = models.ForeignKey(
        TourType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    time = models.DateTimeField()

    guide = models.ForeignKey(
        'guides.TourGuideProfile',
        on_delete=models.CASCADE,
        related_name='tours',
    )

    languages = models.ManyToManyField(
        'utils.Language',
        related_name='tours'
    )

    description = models.TextField(
        max_length=1024,
        blank=True,
        null=True
    )

    duration = models.DecimalField(
        null=True,
        blank=True,
        max_digits=2,
        decimal_places=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal(0)
    )

    meeting_point = models.ForeignKey(
        'utils.Address',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    max_attendees = models.PositiveSmallIntegerField(default=5)

    @property
    def is_free(self):
        return self.price == Decimal(0)

    @property
    def num_of_attendees(self):
        return self.attendees.count()


class Attendee(BaseModel):
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name='attendees'
    )

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='attendances'
    )

    paid = models.DateTimeField(
        null=True,
        blank=True
    )

    refunded = models.DateTimeField(
        null=True,
        blank=True
    )

    kicked_off = models.DateTimeField(
        null=True,
        blank=True
    )


class PersonalTour(BaseModel):
    guide = models.ForeignKey(
        'guides.TourGuideProfile',
        on_delete=models.CASCADE,
        related_name='personal_tours',
    )

    purchaser = models.ForeignKey(
        'users.User',
        related_name='personal_booked_tours',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    users = models.ManyToManyField(
        'users.User',
        related_name='personal_tours'
    )

    time = models.DateTimeField()

    price = models.DecimalField(
        validators=[
            MaxValueValidator(Decimal(1000)),
            MinValueValidator(Decimal(0))
        ],
        default=Decimal(0),
        max_digits=10,
        decimal_places=4
    )

    details = models.TextField(
        max_length=1024,
        null=True,
        blank=True
    )

    paid = models.DateTimeField(
        null=True,
        blank=True
    )

    meeting_point = models.ForeignKey(
        'utils.Address',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


@receiver(pre_save, sender=TourType)
def slugify_tour_type(sender, instance, *args, **kwargs):
    if instance.slug is None or len(instance.slug) == 0:
        org_name = slugify(instance.name)
        instance.slug = org_name
        iteration = 1

        while TourType.objects.filter(slug=instance.slug).exists():
            instance.slug = org_name + '-{}'.format(iteration)
            iteration += 1
