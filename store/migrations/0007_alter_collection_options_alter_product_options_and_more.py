# Generated by Django 5.0.7 on 2024-08-31 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20240721_2346'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title']},
        ),
        migrations.RenameIndex(
            model_name='customer',
            new_name='store_custo_last_na_2e448d_idx',
            old_name='store_custo_last_na_e6a359_idx',
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterModelTable(
            name='customer',
            table='store_customer',
        ),
    ]
