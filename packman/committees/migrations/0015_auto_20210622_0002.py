# Generated by Django 3.2.4 on 2021-06-22 07:02

from django.db import migrations, models
import django.db.models.deletion
import packman.calendars.models


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0004_alter_packyear_options'),
        ('committees', '0014_auto_20210621_2356'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='committeemember',
            options={'ordering': ['year', 'den', 'position', 'member'], 'verbose_name': 'Member', 'verbose_name_plural': 'Members'},
        ),
        migrations.RenameField(
            model_name='committeemember',
            old_name='year_served',
            new_name='year',
        ),
    ]