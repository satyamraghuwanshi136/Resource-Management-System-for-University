# Generated by Django 3.2.8 on 2022-02-05 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_info',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
