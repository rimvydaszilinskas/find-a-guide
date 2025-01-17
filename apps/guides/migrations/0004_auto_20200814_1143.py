# Generated by Django 3.1 on 2020-08-14 11:43

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0003_tourguideprofile_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourguiderating',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tourguiderating',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, unique=True),
        ),
    ]
