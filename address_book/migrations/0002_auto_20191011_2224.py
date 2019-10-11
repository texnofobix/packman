# Generated by Django 2.2.6 on 2019-10-11 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address_book', '0001_initial'),
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumber',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phone_number', to='membership.Member'),
        ),
        migrations.AddField(
            model_name='address',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address', to='membership.Member'),
        ),
    ]
