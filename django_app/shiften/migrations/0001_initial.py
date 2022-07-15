# Generated by Django 4.0.3 on 2022-04-10 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('leden', '0006_alter_lid_media'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shiftlijst',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('shift_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shiften.shiftlijst')),
                ('shifters', models.ManyToManyField(to='leden.lid')),
            ],
        ),
    ]