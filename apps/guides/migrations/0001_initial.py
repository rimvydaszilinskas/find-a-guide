# Generated by Django 3.1 on 2020-08-10 18:00

from decimal import Decimal
from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utils', '0001_initial'),
        ('tours', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TourGuideProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=4, default=Decimal('0'), max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0'))])),
                ('active', models.BooleanField(default=True)),
                ('intro', models.TextField(blank=True, max_length=1024, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('town', models.CharField(max_length=100)),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('languages', models.ManyToManyField(related_name='tour_guides', to='utils.Language')),
                ('tour_types', models.ManyToManyField(related_name='tour_guides', to='tours.TourType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guide_profiles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TourGuideRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('review', models.TextField(blank=True, max_length=1024, null=True)),
                ('guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='guides.tourguideprofile')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='given_ratings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalGuideRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, max_length=1024, null=True)),
                ('processed', models.DateTimeField(blank=True, null=True)),
                ('guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guide_requests', to='guides.tourguideprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guide_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]