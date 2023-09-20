# Generated by Django 3.2.21 on 2023-09-19 21:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('calendars', '0006_alter_category_color_alter_category_description_and_more'),
        ('membership', '0010_alter_family_name_alter_family_pack_comments_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('date_added', models.DateTimeField(auto_now_add=True, help_text='Date and time this entry was first added to the database.', verbose_name='created')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='Date and time this entry was last changed in the database.', verbose_name='modified')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendars.event')),
                ('member', models.ManyToManyField(to='membership.Member')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
