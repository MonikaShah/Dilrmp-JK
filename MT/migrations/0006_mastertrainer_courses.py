# Generated by Django 5.1.6 on 2025-02-27 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MT', '0005_course_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastertrainer',
            name='courses',
            field=models.ManyToManyField(to='MT.course'),
        ),
    ]
