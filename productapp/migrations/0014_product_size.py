# Generated by Django 5.0.7 on 2024-07-27 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0013_remove_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(default=1, max_length=225),
            preserve_default=False,
        ),
    ]