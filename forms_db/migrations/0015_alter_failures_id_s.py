# Generated by Django 4.2.3 on 2023-07-20 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forms_db', '0014_sparepart_remove_failures_errormessage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='failures',
            name='id_s',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='forms_db.station'),
        ),
    ]
