# Generated by Django 3.2.8 on 2022-02-06 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0010_alter_item_info_item_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_info',
            name='item_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
