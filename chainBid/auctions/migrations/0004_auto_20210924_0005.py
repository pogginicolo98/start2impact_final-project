# Generated by Django 3.2.7 on 2021-09-23 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210921_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='hash',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='auction',
            name='tx_id',
            field=models.CharField(blank=True, max_length=66, null=True),
        ),
    ]