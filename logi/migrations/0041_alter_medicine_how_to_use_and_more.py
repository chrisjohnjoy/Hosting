# Generated by Django 4.2.2 on 2024-02-19 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logi', '0040_alter_medicine_medicine_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='how_to_use',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='side_effects',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='uses',
            field=models.TextField(blank=True, null=True),
        ),
    ]
