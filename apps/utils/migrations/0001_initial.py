# Generated by Django 3.1 on 2020-08-10 17:57

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Name')),
                ('address1', models.CharField(blank=True, max_length=256, null=True, verbose_name='Address line 1')),
                ('address2', models.CharField(blank=True, max_length=256, null=True, verbose_name='Address line 2')),
                ('city', models.CharField(blank=True, max_length=128, null=True, verbose_name='City')),
                ('zip_code', models.CharField(blank=True, max_length=12, null=True, verbose_name='ZIP/Postal Code')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('sign', models.CharField(max_length=10)),
                ('exchange_rate', models.DecimalField(decimal_places=4, help_text='Relation to euro', max_digits=10)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('slug', models.SlugField(max_length=100, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('name', models.CharField(db_index=True, max_length=30, unique=True)),
                ('slug', models.CharField(db_index=True, max_length=30, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Languages',
            },
        ),
    ]
