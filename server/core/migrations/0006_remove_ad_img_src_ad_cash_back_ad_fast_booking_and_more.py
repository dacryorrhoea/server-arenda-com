# Generated by Django 5.0.6 on 2024-08-16 09:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_reservation_approve_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='img_src',
        ),
        migrations.AddField(
            model_name='ad',
            name='cash_back',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='fast_booking',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='ad',
            name='long_term',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='count_people',
            field=models.IntegerField(default=6),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.CharField()),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.ad')),
            ],
        ),
    ]
