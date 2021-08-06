# Generated by Django 3.2.4 on 2021-07-15 20:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import localflavor.us.models
import packman.calendars.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('calendars', '0004_alter_packyear_options'),
        ('membership', '0007_auto_20210603_2301'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('sort_order', models.IntegerField(blank=True, null=True, verbose_name='sort order')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('sort_order', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time this entry was first added to the database.', verbose_name='created')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='Date and time this entry was last changed in the database.', verbose_name='modified')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='address')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='city')),
                ('state', localflavor.us.models.USStateField(blank=True, max_length=2, verbose_name='state')),
                ('zipcode', localflavor.us.models.USZipCodeField(blank=True, max_length=10, verbose_name='ZIP code')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='latitude')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='longitude')),
                ('gps_accuracy', models.FloatField(blank=True, null=True, verbose_name='accuracy')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region='US', verbose_name='phone number')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time this entry was first added to the database.', verbose_name='created')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='Date and time this entry was last changed in the database.', verbose_name='modified')),
                ('donation', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='donation')),
                ('notes', models.TextField(blank=True, verbose_name='notes')),
                ('date_paid', models.DateTimeField(blank=True, null=True, verbose_name='paid')),
                ('date_delivered', models.DateTimeField(blank=True, null=True, verbose_name='delivered')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='fundraisers.customer')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='membership.scout')),
                ('year', models.ForeignKey(default=packman.calendars.models.PackYear.get_current, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='calendars.packyear')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time this entry was first added to the database.', verbose_name='created')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='Date and time this entry was last changed in the database.', verbose_name='modified')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('points', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='points')),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='retail value')),
                ('url', models.URLField(blank=True, verbose_name='link')),
                ('year', models.ForeignKey(default=packman.calendars.models.PackYear.get_current, on_delete=django.db.models.deletion.CASCADE, related_name='prizes', to='calendars.packyear')),
            ],
            options={
                'verbose_name': 'Prize',
                'verbose_name_plural': 'Prizes',
                'ordering': ['-year', 'points', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ProductLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time this entry was first added to the database.', verbose_name='created')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='Date and time this entry was last changed in the database.', verbose_name='modified')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_lines', related_query_name='product_line', to='fundraisers.category')),
                ('year', models.ForeignKey(default=packman.calendars.models.PackYear.get_current, on_delete=django.db.models.deletion.CASCADE, related_name='product_lines', related_query_name='product_line', to='calendars.packyear')),
            ],
            options={
                'verbose_name': 'Product Line',
                'verbose_name_plural': 'Product Lines',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time this entry was first added to the database.', verbose_name='created')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='Date and time this entry was last changed in the database.', verbose_name='modified')),
                ('name', models.CharField(max_length=100, verbose_name='title')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='price')),
                ('weight', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name='weight')),
                ('unit', models.CharField(blank=True, choices=[('OZ', 'ounce'), ('LB', 'pound')], max_length=2, verbose_name='measured in')),
                ('sort_order', models.IntegerField(blank=True, null=True, verbose_name='sort order')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='fundraisers.category')),
                ('product_line', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='fundraisers.productline')),
                ('year', models.ForeignKey(default=packman.calendars.models.PackYear.get_current, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='calendars.packyear')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ('sort_order', 'name'),
            },
        ),
        migrations.CreateModel(
            name='PrizeSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time this entry was first added to the database.', verbose_name='created')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='Date and time this entry was last changed in the database.', verbose_name='modified')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='quantity')),
                ('cub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prize_selections', related_query_name='prize_selection', to='membership.scout')),
                ('prize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prize_selections', related_query_name='prize_selection', to='fundraisers.prize')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prize_selections', related_query_name='prize_selection', to='calendars.packyear')),
            ],
            options={
                'verbose_name': 'Prize Selection',
                'verbose_name_plural': 'Prize Selections',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time this entry was first added to the database.', verbose_name='created')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='Date and time this entry was last changed in the database.', verbose_name='modified')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='quantity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', related_query_name='item', to='fundraisers.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', related_query_name='order', to='fundraisers.product')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
