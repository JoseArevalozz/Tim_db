# Generated by Django 4.2.6 on 2023-10-24 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_db', '0015_alter_failures_imgevindence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='failures',
            name='imgEvindence',
            field=models.ImageField(null=True, upload_to='evidences/'),
        ),
    ]