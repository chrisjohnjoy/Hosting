# Generated by Django 4.2.4 on 2023-09-14 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logi', '0002_remove_customer_city_customer_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='date_created',
        ),
    ]
