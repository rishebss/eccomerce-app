# Generated by Django 5.0.7 on 2024-08-27 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0020_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='cat',
            field=models.CharField(max_length=255),
        ),
    ]