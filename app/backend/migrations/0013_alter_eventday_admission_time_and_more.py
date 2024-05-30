# Generated by Django 4.2 on 2024-05-29 10:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_alter_deletedvolunteering_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventday',
            name='admission_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Einlassbeginn'),
        ),
        migrations.AlterField(
            model_name='eventday',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now, unique=True, verbose_name='Veranstaltungsbeginn'),
        ),
        migrations.AlterField(
            model_name='task',
            name='finish_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Ende'),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Beginn'),
        ),
    ]
