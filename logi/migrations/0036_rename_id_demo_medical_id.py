# Generated by Django 4.2.2 on 2024-02-19 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logi', '0035_alter_demo_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demo',
            old_name='id',
            new_name='medical_id',
        ),
    ]
