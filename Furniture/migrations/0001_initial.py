# Generated by Django 3.2.8 on 2022-02-22 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Iteminfo',
            fields=[
                ('item_id', models.IntegerField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(blank=True, max_length=100)),
                ('company', models.CharField(max_length=50)),
                ('purchase_date', models.DateField()),
                ('qty', models.IntegerField(default=1)),
                ('Pur_from', models.CharField(max_length=50)),
                ('order_ref', models.CharField(max_length=50)),
                ('order_date', models.DateField()),
                ('in_no', models.IntegerField()),
                ('spec', models.CharField(max_length=50)),
                ('warn', models.DateField()),
                ('ind_pri', models.IntegerField()),
                ('auth', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Replaceitem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=1)),
                ('date', models.DateField()),
                ('added_by', models.ForeignKey(null='True', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Furniture.iteminfo')),
            ],
        ),
        migrations.CreateModel(
            name='Removeitem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=1)),
                ('date', models.DateField()),
                ('added_by', models.ForeignKey(null='True', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Furniture.iteminfo')),
            ],
        ),
        migrations.CreateModel(
            name='Maintainitem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=1)),
                ('given', models.CharField(max_length=50)),
                ('add_date', models.DateField()),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Furniture.iteminfo')),
            ],
        ),
        migrations.CreateModel(
            name='Assignitem_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('lab_name', models.CharField(max_length=50, null='True')),
                ('faculty', models.CharField(default='', max_length=50)),
                ('assigned_by', models.CharField(default='', max_length=50)),
                ('assign_date', models.DateField()),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Furniture.iteminfo')),
            ],
        ),
    ]
