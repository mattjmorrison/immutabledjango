# Generated by Django 2.1.5 on 2019-01-10 04:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0003_auto_20190110_0418'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='addresses',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=36), default=list, size=None),
        ),
    ]
