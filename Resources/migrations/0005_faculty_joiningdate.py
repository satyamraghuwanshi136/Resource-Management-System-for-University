# Generated by Django 3.1.3 on 2020-12-14 09:10

from django.db import migrations, models
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('Resources', '0004_auto_20201209_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='JoiningDate',
            field=models.DateField(default=datetime.datetime.now()),
            preserve_default=False,
        ),
    ]
