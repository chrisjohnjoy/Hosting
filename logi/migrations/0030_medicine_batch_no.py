# Generated by Django 4.2.2 on 2024-02-13 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logi', '0029_rename_mrp_medicine_buy_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='batch_no',
            field=models.CharField(default='value', max_length=255),
        ),
    ]
