# Generated by Django 4.2.2 on 2024-02-13 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logi', '0031_rename_added_on_medicine_added_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='prescription',
        ),
    ]
