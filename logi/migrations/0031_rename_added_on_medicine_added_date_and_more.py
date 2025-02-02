# Generated by Django 4.2.2 on 2024-02-13 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logi', '0030_medicine_batch_no'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicine',
            old_name='added_on',
            new_name='added_date',
        ),
        migrations.RenameField(
            model_name='medicine',
            old_name='description',
            new_name='how_it_works',
        ),
        migrations.RenameField(
            model_name='medicine',
            old_name='company_id',
            new_name='manufacturer',
        ),
        migrations.RenameField(
            model_name='medicine',
            old_name='buy_price',
            new_name='mrp',
        ),
        migrations.RenameField(
            model_name='medicine',
            old_name='medicine_type',
            new_name='type_of_sell',
        ),
        migrations.RenameField(
            model_name='medicine',
            old_name='sell_price',
            new_name='wholesale_price',
        ),
        migrations.AddField(
            model_name='medicine',
            name='action_class',
            field=models.CharField(default=12, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicine',
            name='active_status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='medicine',
            name='alternate_medicines',
            field=models.TextField(default=21),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicine',
            name='chemical_class',
            field=models.CharField(default=21, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicine',
            name='habit_forming',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='medicine',
            name='how_to_use',
            field=models.TextField(default=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicine',
            name='prescription',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicine',
            name='salt',
            field=models.CharField(default=12, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicine',
            name='side_effects',
            field=models.TextField(default=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicine',
            name='therapeutic_class',
            field=models.CharField(default=12, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicine',
            name='uses',
            field=models.TextField(default=123),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='medicine',
            name='batch_no',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='exp_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='mfg_date',
            field=models.DateField(),
        ),
    ]
