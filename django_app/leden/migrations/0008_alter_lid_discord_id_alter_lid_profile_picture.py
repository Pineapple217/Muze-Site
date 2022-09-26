# Generated by Django 4.0.5 on 2022-07-19 16:07

from django.db import migrations, models
import leden.models


class Migration(migrations.Migration):

    dependencies = [
        ('leden', '0007_lid_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lid',
            name='discord_id',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lid',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/profile/', validators=[leden.models.file_size]),
        ),
    ]