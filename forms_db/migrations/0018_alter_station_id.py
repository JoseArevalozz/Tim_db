# Generated by Django 4.2.3 on 2023-07-20 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_db', '0017_remove_maintenance_statition_s_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
        ),
    ]
