# Generated by Django 5.0.7 on 2024-09-06 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0029_alter_shop_price'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
