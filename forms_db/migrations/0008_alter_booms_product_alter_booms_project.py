# Generated by Django 4.2.3 on 2023-08-03 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_db', '0007_alter_booms_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booms',
            name='product',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='booms',
            name='project',
            field=models.CharField(choices=[('DELL', 'DELL'), ('PMDU', 'PMDU'), ('1G-SW', '1G-SW')], max_length=20),
        ),
    ]