from decimal import Decimal
from django_countries.fields import CountryField

from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.functional import cached_property

from apps.utils.models import BaseModel


class TourGuideProfile(BaseModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='guide_profiles'
    )

    tour_types = models.ManyToManyField(
        'tours.TourType',
        related_name='tour_guides'
    )

    languages = models.ManyToManyField(
        'utils.Language',
        related_name='tour_guides'
    )

    price = models.DecimalField(
        validators=[
            MinValueValidator(Decimal(0))
        ],
        default=Decimal(0),
        decimal_places=4,
        max_digits=7
    )

    active = models.BooleanField(default=True)

    intro = models.TextField(
        max_length=1024,
        null=True,
        blank=True
    )

    country = CountryField()

    town = models.CharField(
        max_length=100
    )

    point = models.PointField(
        srid=4326,
        null=True,
        blank=True
    )

    approved = models.DateTimeField(
        null=True,
        blank=True
    )

    @property
    def is_approved(self):
        return self.approved is not None

    @property
    def is_free(self) -> bool:
        return self.price == Decimal(0)

    @cached_property
    def total_ratings(self):
        return self.ratings.count()

    @cached_property
    def rating(self):
        if self.total_ratings != 0:
            return sum([rating.rating for rating in self.ratings.all()]) / Decimal(self.total_ratings)
        return None

    def __str__(self):
        return self.user.__str__()


class TourGuideRating(BaseModel):
    guide = models.ForeignKey(
        TourGuideProfile,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    tour = models.ForeignKey(
        'tours.Tour',
        on_delete=models.SET_NULL,
        related_name='ratings',
        null=True,
        blank=True
    )

    personal_tour = models.ForeignKey(
        'tours.PersonalTour',
        on_delete=models.SET_NULL,
        related_name='ratings',
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='given_ratings'
    )

    rating = models.SmallIntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )

    review = models.TextField(
        max_length=1024,
        null=True,
        blank=True
    )


class PersonalGuideRequest(BaseModel):
    guide = models.ForeignKey(
        TourGuideProfile,
        on_delete=models.CASCADE,
        related_name='guide_requests'
    )

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='guide_requests'
    )

    message = models.TextField(
        max_length=1024,
        null=True,
        blank=True
    )

    processed = models.DateTimeField(
        null=True,
        blank=True
    )

    tour = models.OneToOneField(
        'tours.PersonalTour',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    @property
    def is_approved(self):
        return self.processed and self.tour is not None
