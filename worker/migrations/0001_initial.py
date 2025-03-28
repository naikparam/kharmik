# Generated by Django 5.1.4 on 2025-02-17 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('aadhar', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=100)),
                ('date_of_start', models.DateField()),
                ('crop_type', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]
