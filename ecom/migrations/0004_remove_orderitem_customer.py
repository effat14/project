# Generated by Django 5.0.4 on 2024-04-19 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0003_alter_orders_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='customer',
        ),
    ]