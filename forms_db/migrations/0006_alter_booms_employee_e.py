# Generated by Django 4.2.3 on 2023-08-03 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forms_db', '0005_booms_employee_e'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booms',
            name='employee_e',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forms_db.employes'),
        ),
    ]
