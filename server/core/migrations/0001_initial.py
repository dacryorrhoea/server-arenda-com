# Generated by Django 5.0.6 on 2024-07-09 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('data_stay', models.DateField(blank=True)),
                ('data_leave', models.DateField(blank=True)),
                ('member_adults', models.IntegerField()),
                ('number_kids', models.IntegerField()),
                ('animal_check', models.BooleanField()),
                ('price', models.IntegerField()),
                ('short_desc', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('owner', models.IntegerField()),
                ('number_beds', models.IntegerField()),
                ('type_housing', models.CharField(max_length=100)),
                ('square_info', models.IntegerField()),
                ('metro_info', models.CharField(max_length=100)),
                ('img_src', models.CharField(max_length=100)),
            ],
        ),
    ]
