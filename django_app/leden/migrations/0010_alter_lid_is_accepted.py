# Generated by Django 4.0.5 on 2022-07-23 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leden', '0009_alter_lid_options_lid_is_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lid',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
    ]