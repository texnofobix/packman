# Generated by Django 2.2.17 on 2020-11-07 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0012_auto_20201103_1330"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="contentblock",
            name="pages_conte_title_1776ce_idx",
        ),
        migrations.RenameField(
            model_name="contentblock",
            old_name="title",
            new_name="heading",
        ),
        migrations.AddIndex(
            model_name="contentblock",
            index=models.Index(
                fields=["heading", "published_on"],
                name="pages_conte_heading_c47d4b_idx",
            ),
        ),
    ]
