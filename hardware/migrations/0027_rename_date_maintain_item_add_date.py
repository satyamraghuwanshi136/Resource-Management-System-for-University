# Generated by Django 3.2.8 on 2022-02-21 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0026_remove_item_added_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maintain_item',
            old_name='date',
            new_name='add_date',
        ),
    ]
