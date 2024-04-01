# Generated by Django 4.2.5 on 2024-01-29 05:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_project', '0006_order_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(default=datetime.datetime(2024, 1, 29, 5, 6, 8, 28495, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.datetime(2024, 1, 29, 5, 6, 40, 121298, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
