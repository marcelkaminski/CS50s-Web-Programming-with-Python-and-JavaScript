# Generated by Django 3.1.7 on 2021-03-05 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210305_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='bids', to='auctions.Bid'),
        ),
    ]
