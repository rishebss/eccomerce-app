# Generated by Django 5.0.7 on 2024-09-11 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0031_ordercart'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='productapp.ordercart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productapp.shop')),
            ],
        ),
    ]