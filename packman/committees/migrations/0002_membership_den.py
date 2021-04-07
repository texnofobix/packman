# Generated by Django 2.2.14 on 2020-07-30 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("dens", "0001_initial"),
        ("committees", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="membership",
            name="den",
            field=models.ForeignKey(
                blank=True,
                help_text="If the member is a Den Leader, which Den # are they supporting?",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="leadership",
                to="dens.Den",
            ),
        ),
    ]
