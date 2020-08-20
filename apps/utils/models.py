from django_countries.fields import CountryField
import uuid

from django.contrib.gis.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


class BaseModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=True,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True


class Currency(models.Model):
    name = models.CharField(
        max_length=30
    )

    slug = models.SlugField(
        max_length=30,
        db_index=True,
        primary_key=True,
        unique=True
    )

    sign = models.CharField(
        max_length=10
    )

    exchange_rate = models.DecimalField(
        help_text='Relation to euro',
        max_digits=10,
        decimal_places=4
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
    )

    slug = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        primary_key=True
    )

    class Meta:
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name


class HashTag(models.Model):
    slug = models.SlugField(
        max_length=100,
        db_index=True,
        unique=True,
        primary_key=True)

    def __str__(self):
        return "#{}".format(self.slug)


class Address(BaseModel):
    name = models.CharField(
        'Name',
        max_length=256,
        null=True,
        blank=True)

    address1 = models.CharField(
        'Address line 1',
        max_length=256,
        null=True,
        blank=True)

    address2 = models.CharField(
        'Address line 2',
        max_length=256,
        null=True,
        blank=True)

    city = models.CharField(
        'City',
        max_length=128,
        null=True,
        blank=True)

    zip_code = models.CharField(
        'ZIP/Postal Code',
        max_length=12,
        null=True,
        blank=True)

    country = CountryField(
        blank_label='(Select country)', null=True, blank=True)

    point = models.PointField(
        srid=4326,
        null=True,
        blank=True
    )


@receiver(pre_save, sender=Currency)
@receiver(pre_save, sender=Language)
def slugify_model(sender, instance, *args, **kwargs):
    if instance.slug is None or len(instance.slug) == 0:
        org = slugify(instance.name)
        instance.slug = org
        it = 1

        while instance.__class__.objects.filter(slug=instance.slug).exists():
            instance.slug = org + '-{}'.format(it)
            it += 1
