# Generated by Django 5.0.7 on 2024-09-04 20:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0021_alter_shop_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='gen',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
