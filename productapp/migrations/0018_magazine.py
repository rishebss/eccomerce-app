# Generated by Django 5.0.7 on 2024-07-30 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0017_userprofile_details_saved_alter_userprofile_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to='magazine/')),
            ],
        ),
    ]
