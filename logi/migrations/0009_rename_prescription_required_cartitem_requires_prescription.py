# Generated by Django 4.2.4 on 2023-09-18 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logi', '0008_cart_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='prescription_required',
            new_name='requires_prescription',
        ),
    ]
