# Generated by Django 4.0.3 on 2022-04-06 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledenlijst', '0003_rename_geboortedatum_lid_date_of_birth_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lid',
            name='email',
        ),
    ]
