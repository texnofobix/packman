# Generated by Django 3.1.5 on 2021-01-12 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address_book', '0008_auto_20210112_1122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venue',
            old_name='type',
            new_name='categories',
        ),
    ]
