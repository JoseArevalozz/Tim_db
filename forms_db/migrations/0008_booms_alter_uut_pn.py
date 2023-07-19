# Generated by Django 4.2.3 on 2023-07-18 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forms_db', '0007_uut_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booms',
            fields=[
                ('pn', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=125)),
                ('commodity', models.CharField(max_length=50)),
                ('product', models.CharField(max_length=30)),
                ('ubi_logic', models.CharField(max_length=15)),
                ('project', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='uut',
            name='pn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms_db.booms'),
        ),
    ]
