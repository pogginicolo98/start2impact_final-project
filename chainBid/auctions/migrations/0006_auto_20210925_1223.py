# Generated by Django 3.2.7 on 2021-09-25 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210924_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='hash',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='tx_id',
        ),
        migrations.CreateModel(
            name='AuctionReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_file', models.FileField(blank=True, null=True, upload_to='')),
                ('hash', models.CharField(blank=True, max_length=64, null=True)),
                ('tx_id', models.CharField(blank=True, max_length=66, null=True)),
                ('auction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='auctions.auction')),
            ],
        ),
    ]
