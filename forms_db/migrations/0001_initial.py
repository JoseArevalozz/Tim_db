# Generated by Django 4.2.3 on 2023-07-17 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('employee_number', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('employee_name', models.CharField(max_length=100)),
                ('pmd', models.BooleanField(default=False)),
                ('dell', models.BooleanField(default=False)),
                ('switch', models.BooleanField(default=False)),
                ('mail', models.TextField(null=True)),
                ('privileges', models.TextField()),
            ],
        ),
    ]