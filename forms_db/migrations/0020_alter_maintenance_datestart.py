# Generated by Django 4.2.2 on 2023-12-13 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_db', '0019_alter_maintenance_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenance',
            name='dateStart',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
