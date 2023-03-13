# Generated by Django 3.2.15 on 2022-10-20 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0023_contentblock_add_bookmark_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentblock',
            name='bookmark',
            field=models.SlugField(blank=True, help_text='Bookmarks can used to allow readers to jump to specific parts of a webpage.', null=True, verbose_name='bookmark'),
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='heading',
            field=models.CharField(blank=True, max_length=256, verbose_name='section heading'),
        ),
    ]