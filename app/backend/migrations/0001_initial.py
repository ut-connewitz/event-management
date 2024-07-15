# Generated by Django 4.2 on 2024-07-04 12:13

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Telefon')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Personen',
            },
        ),
        migrations.CreateModel(
            name='Act',
            fields=[
                ('act_name', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Aktname')),
                ('person_count', models.PositiveIntegerField(blank=True, null=True, verbose_name='Personenzahl')),
                ('act_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Bild')),
                ('music_sample', models.FileField(blank=True, null=True, upload_to='', verbose_name='Musikbeispiel')),
                ('diet', models.CharField(blank=True, max_length=100, verbose_name='Ernährung')),
                ('act_email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Email')),
                ('act_phone', models.CharField(blank=True, max_length=15, verbose_name='Telefon')),
            ],
            options={
                'verbose_name': 'Ensemble',
                'verbose_name_plural': 'Ensembles',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Datum')),
                ('start_time', models.TimeField(default=django.utils.timezone.now, verbose_name='Veranstaltungsbeginn')),
                ('duration', models.DurationField(blank=True, null=True, verbose_name='Veranstaltungsdauer')),
                ('admission_time', models.TimeField(blank=True, null=True, verbose_name='Einlassbeginn')),
            ],
            options={
                'verbose_name': 'Veranstaltung',
                'verbose_name_plural': 'Veranstaltungen',
            },
        ),
        migrations.CreateModel(
            name='EventSeries',
            fields=[
                ('event_name', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Veranstaltungsname')),
                ('event_type', models.CharField(choices=[('CI', 'Kino'), ('CO', 'Musik'), ('PL', 'Bühne'), ('PY', 'Party'), ('EX', 'Extra'), ('FV', 'Festival'), ('OT', 'Sonstiges')], default='OT', max_length=2, verbose_name='Veranstaltungsart')),
                ('event_description', models.TextField(blank=True, verbose_name='Beschreibung')),
                ('event_press', models.TextField(blank=True, verbose_name='Pressetext')),
                ('event_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Einlassgebühr')),
                ('event_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Bild')),
            ],
            options={
                'verbose_name': 'Veranstaltungsreihe',
                'verbose_name_plural': 'Veranstaltungsreihen',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notification_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('notification_type', models.CharField(choices=[('AB', 'Aufgabenbenachrichtigung'), ('DB', 'Dienstbenachrichtigung'), ('BN', 'Benachrichtigung')], default='BN', max_length=2, verbose_name='Benachrichtigungsart')),
                ('comment', models.TextField(blank=True, verbose_name='Kommentar')),
                ('timer', models.PositiveIntegerField(verbose_name='Timer')),
            ],
            options={
                'verbose_name': 'Benachrichtigung',
                'verbose_name_plural': 'Benachrichtigungen',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('setting_name', models.CharField(primary_key=True, serialize=False, verbose_name='Einstellungsname')),
                ('setting_type', models.CharField(choices=[('NG', 'Benachrichtigungen allgmein'), ('NS', 'Bestimmte Benachrichtigung'), ('AP', 'Erscheinungsbild'), ('ST', 'Einstellung')], default='ST', max_length=2, verbose_name='Einstellungsart')),
                ('value_type', models.CharField(choices=[('BO', 'Bool'), ('IN', 'Integer'), ('EN', 'Eumeration')], default='BO', max_length=2, verbose_name='Datentyp')),
            ],
            options={
                'verbose_name': 'Einstellung',
                'verbose_name_plural': 'Einstellungen',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('task_type', models.CharField(choices=[('AD', 'Einlass'), ('TT', 'Tontechnik'), ('LT', 'Lichttechnik'), ('KÜ', 'Küche'), ('BR', 'Bar'), ('OT', 'Sonstiges')], default='OT', max_length=2, verbose_name='Aufgabenart')),
                ('team_restriction', models.CharField(choices=[('TT', 'Tontechnik'), ('LT', 'Lichttechnik'), ('VW', 'Verwaltung'), ('NO', 'Ohne')], default='NO', max_length=2, verbose_name='Teambindung')),
                ('urgency', models.CharField(choices=[('UR', 'Dringend'), ('IM', 'Wichtig'), ('MD', 'Mittel'), ('LO', 'Niedrig')], default='MD', max_length=2, verbose_name='Dringlichkeit')),
                ('state', models.CharField(choices=[('FR', 'Offen'), ('TK', 'Übernommen'), ('MB', 'Vielleicht'), ('DN', 'Erledigt')], default='FR', editable=False, max_length=2, verbose_name='Status')),
                ('start_time', models.TimeField(blank=True, null=True, verbose_name='Beginn')),
                ('finish_time', models.TimeField(blank=True, null=True, verbose_name='Ende')),
                ('comment', models.TextField(blank=True, verbose_name='Kommentar')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.event', verbose_name='Veranstaltung')),
            ],
            options={
                'verbose_name': 'Aufgabe',
                'verbose_name_plural': 'Aufgaben',
            },
        ),
        migrations.CreateModel(
            name='UserSettingValue',
            fields=[
                ('user_setting_value_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.setting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Einstellungswert',
                'verbose_name_plural': 'Einstellungswerte',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('street', models.CharField(blank=True, max_length=40, verbose_name='Straße')),
                ('house_number', models.CharField(blank=True, max_length=40, verbose_name='Hausnummer')),
                ('postal_code', models.CharField(blank=True, max_length=40, verbose_name='PLZ')),
                ('country', models.CharField(blank=True, max_length=40, verbose_name='Land')),
            ],
            options={
                'verbose_name': 'Adresse',
                'verbose_name_plural': 'Adressen',
            },
        ),
        migrations.CreateModel(
            name='BoolValue',
            fields=[
                ('usersettingvalue_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.usersettingvalue')),
                ('bool_value', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Boolwert',
                'verbose_name_plural': 'Boolwerte',
            },
            bases=('backend.usersettingvalue',),
        ),
        migrations.CreateModel(
            name='EnumValue',
            fields=[
                ('usersettingvalue_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.usersettingvalue')),
            ],
            options={
                'verbose_name': 'Enumwert',
                'verbose_name_plural': 'Enumwerte',
            },
            bases=('backend.usersettingvalue',),
        ),
        migrations.CreateModel(
            name='IntValue',
            fields=[
                ('usersettingvalue_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.usersettingvalue')),
                ('int_value', models.BigIntegerField()),
            ],
            options={
                'verbose_name': 'Integerwert',
                'verbose_name_plural': 'Integerwerte',
            },
            bases=('backend.usersettingvalue',),
        ),
        migrations.CreateModel(
            name='TaskNotification',
            fields=[
                ('notification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.notification')),
            ],
            options={
                'verbose_name': 'Aufgabenbenachrichtigung',
                'verbose_name_plural': 'Aufgabenbenachrichtigungen',
            },
            bases=('backend.notification',),
        ),
        migrations.CreateModel(
            name='Volunteering',
            fields=[
                ('volunteering_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('confirmation_type', models.CharField(choices=[('NO', 'Nein'), ('YS', 'Ja')], default='YS', max_length=15, verbose_name='Zusage')),
                ('comment', models.TextField(blank=True, max_length=300, verbose_name='Kommentar')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.task', verbose_name='Aufgabe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Person')),
            ],
            options={
                'verbose_name': 'Dienst',
                'verbose_name_plural': 'Dienste',
            },
        ),
        migrations.CreateModel(
            name='UTMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_number', models.PositiveIntegerField(verbose_name='Mitgliedsnummer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Person')),
            ],
            options={
                'verbose_name': 'Vereinsmitglied',
                'verbose_name_plural': 'Vereinsmitglieder',
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('team_member_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.team', verbose_name='Team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Person')),
            ],
            options={
                'verbose_name': 'Teammitgliedschaft',
                'verbose_name_plural': 'Teammitgliedschaften',
            },
        ),
        migrations.CreateModel(
            name='EventAct',
            fields=[
                ('event_act_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('act', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.act', verbose_name='Ensemble')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.event', verbose_name='Veranstaltung')),
            ],
            options={
                'verbose_name': 'Auftritt',
                'verbose_name_plural': 'Auftritte',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.eventseries', verbose_name='Veranstaltungsreihe'),
        ),
        migrations.CreateModel(
            name='DeletedVolunteering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='Zeitpunkt')),
                ('comment', models.TextField(blank=True, max_length=300, verbose_name='Kommentar')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.task', verbose_name='Aufgabe')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Person')),
            ],
            options={
                'verbose_name': 'Gelöschter Dienst',
                'verbose_name_plural': 'Gelöschte Dienste',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='Teams zu welchen die Person gehört. Alle Befugnisse einer Gruppe gehen auf die Person über', related_name='user_set', related_query_name='user', through='backend.TeamMember', to='backend.team'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='VolunteeringNotification',
            fields=[
                ('notification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.notification')),
                ('volunteering', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.volunteering')),
            ],
            options={
                'verbose_name': 'Dienstbenachrichtigung',
                'verbose_name_plural': 'Dienstbenachrichtigungen',
            },
            bases=('backend.notification',),
        ),
        migrations.AddConstraint(
            model_name='volunteering',
            constraint=models.UniqueConstraint(fields=('task',), name='prevent multiple volunteerings for one task constraint'),
        ),
        migrations.AddConstraint(
            model_name='utmember',
            constraint=models.UniqueConstraint(fields=('member_number',), name='member_number is unique'),
        ),
        migrations.AddConstraint(
            model_name='teammember',
            constraint=models.UniqueConstraint(fields=('user', 'team'), name='prevent multiple memberships of one person in one team constraint'),
        ),
        migrations.AddField(
            model_name='tasknotification',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.task'),
        ),
        migrations.AddConstraint(
            model_name='eventact',
            constraint=models.UniqueConstraint(fields=('event', 'act'), name='prevent multiple shows by one act at one event constraint'),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.UniqueConstraint(fields=('date', 'start_time'), name='prevent event duplicates constraint'),
        ),
        migrations.AddConstraint(
            model_name='deletedvolunteering',
            constraint=models.UniqueConstraint(fields=('task',), name='prevent multiple deleted volunteerings for one task constraint'),
        ),
    ]
