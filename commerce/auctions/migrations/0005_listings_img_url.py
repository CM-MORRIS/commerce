# Generated by Django 3.1.2 on 2020-10-26 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listings_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='IMG_URL',
            field=models.CharField(default='127.0.0.1:8000', max_length=1000),
            preserve_default=False,
        ),
    ]