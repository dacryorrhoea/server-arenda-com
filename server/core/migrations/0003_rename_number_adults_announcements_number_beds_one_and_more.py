# Generated by Django 5.0.6 on 2024-07-10 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_announcements_delete_announcement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='announcements',
            old_name='number_adults',
            new_name='number_beds_one',
        ),
        migrations.RenameField(
            model_name='announcements',
            old_name='number_beds',
            new_name='number_beds_two',
        ),
        migrations.RenameField(
            model_name='announcements',
            old_name='number_kids',
            new_name='number_people',
        ),
        migrations.RemoveField(
            model_name='announcements',
            name='data_leave',
        ),
        migrations.RemoveField(
            model_name='announcements',
            name='data_stay',
        ),
        migrations.AddField(
            model_name='announcements',
            name='time_leave',
            field=models.CharField(default=115555, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='announcements',
            name='time_stay',
            field=models.CharField(default=115555, max_length=100),
            preserve_default=False,
        ),
    ]
