# Generated by Django 2.2.16 on 2020-10-30 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20201030_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.TextField(blank=True, default='', help_text='Brief description of what the document is.'),
        ),
    ]
