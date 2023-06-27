# Generated by Django 3.2.19 on 2023-06-26 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dens', '0011_alter_rank_rank'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='membership',
            constraint=models.UniqueConstraint(fields=('scout', 'year_assigned'), name='unique_membership_year'),
        ),
    ]
