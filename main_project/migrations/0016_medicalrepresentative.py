# Generated by Django 4.2.5 on 2024-02-06 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logi', '0025_user_is_medical_representative'),
        ('main_project', '0015_remove_purchaseorder_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalRepresentative',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', models.CharField(max_length=20)),
                ('designation', models.CharField(max_length=30)),
                ('company_name', models.CharField(max_length=50)),
            ],
        ),
    ]
