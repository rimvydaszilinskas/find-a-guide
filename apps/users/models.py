from django_countries.fields import CountryField
import pytz

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property

from apps.utils.models import BaseModel
from apps.utils.storage import OverwriteStorage

from .managers import UserManager
from .utils import profile_picture_upload_util, generate_verification_string


class User(AbstractUser, BaseModel):
    username = models.CharField(
        max_length=30, null=True, blank=True, unique=True)

    email = models.EmailField(unique=True, db_index=True)

    timezone = models.CharField(max_length=50, choices=(
        (zone, zone) for zone in pytz.all_timezones), default='Europe/Copenhagen')

    verification_string = models.CharField(
        max_length=50, default=generate_verification_string)

    currency = models.ForeignKey(
        'utils.Currency',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to=profile_picture_upload_util,
        storage=OverwriteStorage(),
        null=True,
        blank=True
    )

    languages = models.ManyToManyField(
        'utils.Language',
        related_name='user_profiles',
        blank=True
    )

    intro = models.TextField(
        max_length=1024,
        null=True,
        blank=True
    )

    origin_country = CountryField(
        null=True,
        blank=True
    )

    origin_town = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    @cached_property
    def is_guide(self):
        return self.user.guide_profiles.exists()

    def __str__(self):
        return self.user.__str__()


@receiver(post_save, sender=User)
def create_profile(sender, instance, *args, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
