# Generated by Django 4.2 on 2024-06-21 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_alter_task_event_alter_task_task_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teammember',
            options={'verbose_name': 'Teammitgliedschaft', 'verbose_name_plural': 'Teammitgliedschaften'},
        ),
        migrations.AlterModelOptions(
            name='utmember',
            options={'verbose_name': 'Vereinsmitglied', 'verbose_name_plural': 'Vereinsmitglieder'},
        ),
        migrations.RemoveConstraint(
            model_name='deletedvolunteering',
            name='prevent multiple deletd volunteerings for one task constraint',
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='Teams zu welchen die Person gehört. Alle Befugnisse einer Gruppe gehen auf die Person über', through='backend.TeamMember', to='backend.team'),
        ),
        migrations.AddConstraint(
            model_name='deletedvolunteering',
            constraint=models.UniqueConstraint(fields=('task',), name='prevent multiple deleted volunteerings for one task constraint'),
        ),
    ]