# Generated by Django 4.2.4 on 2023-09-18 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logi', '0007_remove_cartitem_user_cartitem_prescription_required_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
