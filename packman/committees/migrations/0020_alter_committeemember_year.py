# Generated by Django 4.2.3 on 2023-07-07 18:45

from django.db import migrations, models
import django.db.models.deletion
import packman.calendars.models


class Migration(migrations.Migration):
    dependencies = [
        ("calendars", "0006_alter_category_color_alter_category_description_and_more"),
        ("committees", "0019_alter_committee_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="committeemember",
            name="year",
            field=models.ForeignKey(
                default=packman.calendars.models.PackYear.get_current,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="committee_memberships",
                related_query_name="committee_membership",
                to="calendars.packyear",
                verbose_name="year served",
            ),
        ),
    ]