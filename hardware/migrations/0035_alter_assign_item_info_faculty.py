# Generated by Django 3.2.8 on 2022-03-02 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Resources', '0005_faculty_joiningdate'),
        ('hardware', '0034_alter_item_info_auth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assign_item_info',
            name='faculty',
            field=models.ForeignKey(null='True', on_delete=django.db.models.deletion.DO_NOTHING, to='Resources.faculty'),
        ),
    ]