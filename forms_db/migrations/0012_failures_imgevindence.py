# Generated by Django 4.2.3 on 2023-08-07 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_db', '0011_alter_failures_shiftfailure_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='failures',
            name='imgEvindence',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]