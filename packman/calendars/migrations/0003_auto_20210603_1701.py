# Generated by Django 3.2.2 on 2021-06-04 00:01

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0002_auto_20210221_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time this entry was first added to the database.', verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='category',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, help_text='Date and time this entry was last changed in the database.', verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='category',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time this entry was first added to the database.', verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='event',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, help_text='Date and time this entry was last changed in the database.', verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='event',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID'),
        ),
    ]
