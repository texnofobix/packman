# Generated by Django 2.2.17 on 2020-11-03 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post_office', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='to_field',
        ),
    ]
