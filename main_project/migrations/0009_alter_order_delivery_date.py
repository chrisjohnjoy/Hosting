# Generated by Django 4.2.5 on 2024-01-29 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_project', '0008_alter_order_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(null=True),
        ),
    ]
