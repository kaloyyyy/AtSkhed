# Generated by Django 5.0.1 on 2024-03-04 03:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignsection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'assignSection',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('classid', models.AutoField(db_column='classID', primary_key=True, serialize=False)),
                ('classsection', models.TextField(db_column='classSection')),
            ],
            options={
                'db_table': 'classes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Classrooms',
            fields=[
                ('classroomid', models.AutoField(db_column='classroomID', primary_key=True, serialize=False)),
                ('room_name', models.TextField(db_column='roomName')),
                ('floor', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('bldg', models.TextField()),
                ('type', models.TextField()),
            ],
            options={
                'db_table': 'classrooms',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Classroomschedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'classroomSchedule',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('courseid', models.AutoField(db_column='courseID', primary_key=True, serialize=False)),
                ('code', models.TextField(unique=True)),
                ('description', models.TextField()),
                ('units', models.FloatField()),
            ],
            options={
                'db_table': 'courses',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Timeslots',
            fields=[
                ('timeid', models.AutoField(db_column='timeID', primary_key=True, serialize=False)),
                ('timestart', models.TextField(db_column='timeStart')),
                ('timeend', models.TextField(db_column='timeEnd')),
                ('day', models.IntegerField()),
            ],
            options={
                'db_table': 'timeSlots',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Programs',
            fields=[
                ('programid', models.AutoField(db_column='programID', primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('firstyears', models.IntegerField(db_column='firstYears')),
                ('secondyears', models.IntegerField(db_column='secondYears')),
                ('thirdyears', models.IntegerField(db_column='thirdYears')),
                ('fourthyears', models.IntegerField(db_column='fourthYears')),
                ('groupfirstyear', models.IntegerField(db_column='groupFirstYear')),
                ('groupsecondyear', models.IntegerField(db_column='groupSecondYear')),
                ('groupthirdyear', models.IntegerField(db_column='groupThirdYear')),
                ('groupfourthyear', models.IntegerField(db_column='groupFourthYear')),
            ],
            options={
                'db_table': 'programs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Prospectus',
            fields=[
                ('prospectusid', models.AutoField(db_column='prospectusID', primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('semester', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'prospectus',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rleschedule',
            fields=[
                ('rleid', models.AutoField(db_column='rleID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'rleSchedule',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('sectionid', models.AutoField(db_column='sectionID', primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('section', models.TextField()),
            ],
            options={
                'db_table': 'sections',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring00',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_0',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring01',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_1',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring010',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_10',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring011',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_11',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring012',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_12',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring013',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_13',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring014',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_14',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring015',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_15',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring016',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_16',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring017',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_17',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring018',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_18',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring019',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_19',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring02',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_2',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring03',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_3',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring04',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_4',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring05',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_5',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring06',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_6',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring07',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_7',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring08',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_8',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offspring09',
            fields=[
                ('timeid', models.OneToOneField(db_column='timeID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='schedsite.timeslots')),
            ],
            options={
                'db_table': 'offspring_0_9',
                'managed': False,
            },
        ),
    ]
