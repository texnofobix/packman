# Generated by Django 3.2.2 on 2021-06-03 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0018_auto_20210603_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]