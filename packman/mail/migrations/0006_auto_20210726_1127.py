# Generated by Django 3.2.4 on 2021-07-26 18:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0005_alter_listsettings_list_from'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listsettings',
            name='list_description',
        ),
        migrations.RemoveField(
            model_name='listsettings',
            name='list_from',
        ),
        migrations.RemoveField(
            model_name='listsettings',
            name='list_help',
        ),
        migrations.RemoveField(
            model_name='listsettings',
            name='list_name',
        ),
        migrations.RemoveField(
            model_name='listsettings',
            name='list_subject',
        ),
        migrations.AddField(
            model_name='listsettings',
            name='from_email',
            field=models.EmailField(blank=True, help_text='The email address that emails sent from this list will originate from.', max_length=254, verbose_name='from email'),
        ),
        migrations.AddField(
            model_name='listsettings',
            name='from_name',
            field=models.CharField(blank=True, help_text='The name that will be displayed in the From line of emails sent from this list.', max_length=40, verbose_name='from name'),
        ),
        migrations.AddField(
            model_name='listsettings',
            name='help_email',
            field=models.EmailField(blank=True, help_text='An email address that members should be able to contact in the event they require assistance with the delivery of emails from the list.', max_length=254, verbose_name='help email'),
        ),
        migrations.AddField(
            model_name='listsettings',
            name='name',
            field=models.CharField(blank=True, help_text='An optional descriptive name for emails generated by this application.', max_length=100, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='listsettings',
            name='subject_prefix',
            field=models.CharField(blank=True, help_text="If provided, the subject prefix will preceed every sent email's subject in the email subject field.", max_length=20, verbose_name='subject line prefix'),
        ),
        migrations.AlterField(
            model_name='listsettings',
            name='list_id',
            field=models.CharField(help_text='A List-Id will be included in the header of any email sent from this application. The List-Id should be unique to the list and clearly identify your organization (e.g. lists.example.com).', max_length=100, validators=[django.core.validators.URLValidator], verbose_name='list ID'),
        ),
    ]
