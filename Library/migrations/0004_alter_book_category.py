# Generated by Django 3.2.7 on 2021-12-04 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0003_alter_book_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('education', 'Education'), ('Data Structure', 'Data Structure'), ('Computer Network', 'Computer Network'), ('Software Engineering', 'Software Engineering'), ('Database Management System', 'Database Management System'), ('Operating System', 'Operating System'), ('Information Security', 'Information Security'), ('Analysis and design of Algorithms', 'Analysis and design of Algorithms'), ('Machine Learning', 'Machine Learning')], default='education', max_length=50),
        ),
    ]