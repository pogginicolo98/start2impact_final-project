# Generated by Django 3.2.7 on 2021-09-24 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20210924_0005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auction',
            options={'ordering': ['-opened_at', 'title'], 'verbose_name': 'Auction', 'verbose_name_plural': 'Auctions'},
        ),
        migrations.RenameField(
            model_name='auction',
            old_name='opening_date',
            new_name='opened_at',
        ),
        migrations.RenameField(
            model_name='auction',
            old_name='won_by',
            new_name='winner',
        ),
    ]