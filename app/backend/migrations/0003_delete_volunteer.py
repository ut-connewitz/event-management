# Generated by Django 4.2 on 2024-04-18 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_utmember_member_number_is_unique'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Volunteer',
        ),
    ]