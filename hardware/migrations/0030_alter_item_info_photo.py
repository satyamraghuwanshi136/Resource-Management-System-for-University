# Generated by Django 3.2.8 on 2022-02-23 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0029_alter_item_info_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_info',
            name='photo',
            field=models.ImageField(upload_to='img/%y'),
        ),
    ]
