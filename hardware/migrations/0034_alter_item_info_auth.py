# Generated by Django 3.2.8 on 2022-03-02 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0033_auto_20220302_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_info',
            name='auth',
            field=models.CharField(max_length=50),
        ),
    ]
