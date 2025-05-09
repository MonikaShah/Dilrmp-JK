# Generated by Django 5.1.6 on 2025-04-07 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MT', '0009_rename_created_at_mastertrainerfeedback_submitted_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MTRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mt_id', models.CharField(max_length=20)),
                ('district', models.CharField(max_length=100)),
                ('datetime', models.DateTimeField()),
                ('photo', models.ImageField(upload_to='mt_photos/')),
            ],
        ),
    ]
