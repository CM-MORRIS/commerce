# Generated by Django 3.1.1 on 2020-10-19 21:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listings',
            fields=[
                ('listing_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('starting_price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('start_date', models.DateTimeField(default=datetime.datetime(2020, 10, 19, 21, 16, 47, 552846, tzinfo=utc))),
                ('end_date', models.DateTimeField(default=datetime.datetime(2020, 10, 19, 21, 16, 47, 552875, tzinfo=utc))),
                ('is_sold', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=1000)),
                ('listing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listings')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('bid_id', models.AutoField(primary_key=True, serialize=False)),
                ('bid_price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('listing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listings')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]