# Generated by Django 5.0.7 on 2024-10-03 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_order_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['user__first_name', 'user__last_name'], 'permissions': [('view_history', 'Can view history')]},
        ),
    ]
