# Generated by Django 5.1.6 on 2025-02-25 09:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MT', '0003_alter_mastertrainer_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mastertrainer',
            old_name='deatils_experience',
            new_name='experience_details',
        ),
        migrations.AddField(
            model_name='mastertrainer',
            name='regis_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
