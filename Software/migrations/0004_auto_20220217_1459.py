# Generated by Django 3.2.8 on 2022-02-17 09:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Software', '0003_software_manage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='software_info',
            name='ValD',
        ),
        migrations.RemoveField(
            model_name='software_info',
            name='id',
        ),
        migrations.RemoveField(
            model_name='software_manage',
            name='SName',
        ),
        migrations.AddField(
            model_name='software_info',
            name='Soft_id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='software_info',
            name='auth',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='software_info',
            name='ind_pri',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='software_manage',
            name='Keys',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='software_manage',
            name='Soft_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='Software.software_info'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='software_manage',
            name='assign_date',
            field=models.DateField(default=datetime.date(2022, 2, 17)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='software_manage',
            name='assigned_by',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='software_manage',
            name='LabI',
            field=models.CharField(max_length=20),
        ),
    ]
