# Generated by Django 4.2.3 on 2023-07-07 18:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calendars", "0005_auto_20210720_1640"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="color",
            field=models.CharField(
                blank=True,
                choices=[
                    ("primary", "Blue"),
                    ("success", "Green"),
                    ("danger", "Red"),
                    ("warning", "Yellow"),
                    ("info", "Teal"),
                    ("secondary", "Grey/Muted"),
                    ("transparent", "Transparent"),
                ],
                help_text="Optionally choose a color to display these event in.",
                max_length=16,
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="description",
            field=models.CharField(
                blank=True,
                help_text="Give a little more detail about the kinds of events in this category",
                max_length=256,
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="icon",
            field=models.CharField(
                blank=True,
                choices=[
                    ('<i class="fas fa-award"></i>', "Award"),
                    ('<i class="fas fa-bell"></i>', "Bell"),
                    ('<i class="fas fa-calendar-alt"></i>', "Calendar"),
                    ('<i class="fas fa-campground"></i>', "Campground"),
                    ('<i class="fas fa-times-circle"></i>', "Circled 'X'"),
                    ('<i class="fas fa-donate"></i>', "Donate"),
                    ('<i class="fas fa-exclamation-triangle"></i>', "Exclamation"),
                    ('<i class="fas fa-gift"></i>', "Gift box"),
                    ('<i class="fas fa-users"></i>', "Group (large)"),
                    ('<i class="fas fa-user-friends"></i>', "Group (small)"),
                    ('<i class="fas fa-hands-helping"></i>', "Hands Helping"),
                    ('<i class="fas fa-handshake"></i>', "Hands Shaking"),
                    ('<i class="fas fa-heart"></i>', "Heart"),
                    ('<i class="fas fa-medal"></i>', "Medal"),
                    ('<i class="fas fa-ribbon"></i>', "Ribbon"),
                    ('<i class="fas fa-desktop"></i>', "Computer Screen"),
                    ('<i class="fas fa-seedling"></i>', "Seedling"),
                    ('<i class="fas fa-star"></i>', "Star"),
                ],
                help_text="Optionally choose an icon to display with these events",
                max_length=64,
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="location",
            field=models.CharField(blank=True, max_length=128),
        ),
    ]