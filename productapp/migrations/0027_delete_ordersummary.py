# Generated by Django 5.0.7 on 2024-09-06 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0026_ordersummary'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderSummary',
        ),
    ]