# Generated by Django 4.2.3 on 2023-07-20 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms_db', '0018_alter_station_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='station',
            old_name='id',
            new_name='idi',
        ),
    ]
