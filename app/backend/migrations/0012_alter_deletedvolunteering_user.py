# Generated by Django 4.2 on 2024-05-29 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_alter_deletedvolunteering_user_alter_task_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletedvolunteering',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Person'),
        ),
    ]