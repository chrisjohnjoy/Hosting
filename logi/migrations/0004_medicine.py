# Generated by Django 4.2.4 on 2023-09-17 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logi', '0003_remove_customer_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('medicine_id', models.AutoField(primary_key=True, serialize=False)),
                ('medicine_name', models.CharField(max_length=255)),
                ('medicine_type', models.CharField(max_length=255)),
                ('buy_price', models.CharField(max_length=255)),
                ('sell_price', models.CharField(max_length=255)),
                ('batch_no', models.CharField(max_length=255)),
                ('mfg_date', models.DateField()),
                ('exp_date', models.DateField()),
                ('company_id', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('in_stock', models.IntegerField()),
                ('added_on', models.DateField()),
                ('medicine_image', models.ImageField(upload_to='medicine_images/')),
            ],
        ),
    ]
