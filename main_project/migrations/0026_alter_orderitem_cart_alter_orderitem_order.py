# Generated by Django 4.2.5 on 2024-03-05 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logi', '0044_remove_medicalrepresentative_total_quantity_sold_and_more'),
        ('main_project', '0025_alter_orderitem_cart_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logi.cart'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_project.order'),
        ),
    ]
