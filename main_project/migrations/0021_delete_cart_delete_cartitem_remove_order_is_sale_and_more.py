# Generated by Django 4.2.5 on 2024-02-28 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_project', '0020_cart_cartitem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_sale',
        ),
        migrations.RemoveField(
            model_name='order',
            name='profit_margin',
        ),
    ]
