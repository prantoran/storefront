# Generated by Django 5.0.7 on 2024-09-20 06:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_cartitem_cart_alter_cartitem_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
