# Generated by Django 4.2 on 2024-07-27 12:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_team_prevent_teamname_duplicates_constraint'),
    ]

    operations = [
        migrations.CreateModel(
            name='PastEvent',
            fields=[
                ('past_event_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Datum')),
                ('start_time', models.TimeField(default=django.utils.timezone.now, verbose_name='Veranstaltungsbeginn')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.eventseries', verbose_name='Veranstaltungsreihe')),
            ],
            options={
                'verbose_name': 'Vergangene Veranstaltung',
                'verbose_name_plural': 'Vergangene Veranstaltungen',
                'ordering': ['date'],
            },
        ),
    ]
