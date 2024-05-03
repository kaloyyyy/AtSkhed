from django.db import models


class Assignsection(models.Model):
    sectionid = models.ForeignKey('Sections', models.DO_NOTHING, db_column='sectionID', to_field=None, blank=True,
                                  null=True)  # Field name made lowercase.
    classid = models.ForeignKey('Classes', models.DO_NOTHING, db_column='classID', to_field=None, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'assignSection'


class Classes(models.Model):
    class_id = models.AutoField(db_column='class_id', primary_key=True, blank=True,
                                null=False)  # Field name made lowercase.
    prospectus_id = models.ForeignKey('Prospectus', models.DO_NOTHING, db_column='prospectus_id', to_field=None,
                                      blank=True, null=True)  # Field name made lowercase.
    classroom_id = models.ForeignKey('Classrooms', models.DO_NOTHING, db_column='classroom_id', to_field=None, blank=True,
                                    null=True)  # Field name made lowercase.
    class_section_letter = models.TextField(db_column='class_section_letter', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'classes'


class Classroomschedule(models.Model):
    timeid = models.ForeignKey('Timeslots', models.DO_NOTHING, db_column='timeID',
                               to_field=None)  # Field name made lowercase.
    amphi = models.ForeignKey(Classes, models.DO_NOTHING, db_column='AMPHI', related_name='classroomschedule_amphi_set',
                              blank=True, null=False)  # Field name made lowercase.
    nutrilab = models.ForeignKey(Classes, models.DO_NOTHING, db_column='NUTRILAB',
                                 related_name='classroomschedule_nutrilab_set', blank=True,
                                 null=False)  # Field name made lowercase.
    bc203 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='BC203', related_name='classroomschedule_bc203_set',
                              blank=True, null=False)  # Field name made lowercase.
    bc304 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='BC304', related_name='classroomschedule_bc304_set',
                              blank=True, null=False)  # Field name made lowercase.
    bc305 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='BC305', related_name='classroomschedule_bc305_set',
                              blank=True, null=False)  # Field name made lowercase.
    bc307_table_type = models.ForeignKey(Classes, models.DO_NOTHING, db_column='BC307_table_type',
                                         related_name='classroomschedule_bc307_table_type_set', blank=True,
                                         null=False)  # Field name made lowercase.
    bc308 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='BC308', related_name='classroomschedule_bc308_set',
                              blank=True, null=False)  # Field name made lowercase.
    bc401 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='BC401', related_name='classroomschedule_bc401_set',
                              blank=True, null=False)  # Field name made lowercase.
    bc402 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='BC402', related_name='classroomschedule_bc402_set',
                              blank=True, null=False)  # Field name made lowercase.
    bc403 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='BC403', related_name='classroomschedule_bc403_set',
                              blank=True, null=False)  # Field name made lowercase.
    bc405 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='BC405', related_name='classroomschedule_bc405_set',
                              blank=True, null=False)  # Field name made lowercase.
    bc406 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='BC406', related_name='classroomschedule_bc406_set',
                              blank=True, null=False)  # Field name made lowercase.
    bc407 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='BC407', related_name='classroomschedule_bc407_set',
                              blank=True, null=False)  # Field name made lowercase.
    bc408 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='BC408', related_name='classroomschedule_bc408_set',
                              blank=True, null=False)  # Field name made lowercase.
    bc409_prc_rm = models.ForeignKey(Classes, models.DO_NOTHING, db_column='BC409_PRC_rm',
                                     related_name='classroomschedule_bc409_prc_rm_set', blank=True,
                                     null=False)  # Field name made lowercase.
    c108_lab = models.ForeignKey(Classes, models.DO_NOTHING, db_column='C108_lab',
                                 related_name='classroomschedule_c108_lab_set', blank=True,
                                 null=False)  # Field name made lowercase.
    c110_lab = models.ForeignKey(Classes, models.DO_NOTHING, db_column='C110_lab',
                                 related_name='classroomschedule_c110_lab_set', blank=True,
                                 null=False)  # Field name made lowercase.
    c205_lab = models.ForeignKey(Classes, models.DO_NOTHING, db_column='C205_lab',
                                 related_name='classroomschedule_c205_lab_set', blank=True,
                                 null=False)  # Field name made lowercase.
    c206_lab = models.ForeignKey(Classes, models.DO_NOTHING, db_column='C206_lab',
                                 related_name='classroomschedule_c206_lab_set', blank=True,
                                 null=False)  # Field name made lowercase.
    c209_lab = models.ForeignKey(Classes, models.DO_NOTHING, db_column='C209_lab',
                                 related_name='classroomschedule_c209_lab_set', blank=True,
                                 null=False)  # Field name made lowercase.
    c308_lab = models.ForeignKey(Classes, models.DO_NOTHING, db_column='C308_lab',
                                 related_name='classroomschedule_c308_lab_set', blank=True,
                                 null=False)  # Field name made lowercase.
    c310_lab = models.ForeignKey(Classes, models.DO_NOTHING, db_column='C310_lab',
                                 related_name='classroomschedule_c310_lab_set', blank=True,
                                 null=False)  # Field name made lowercase.
    c311 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='C311', related_name='classroomschedule_c311_set',
                             blank=True, null=False)  # Field name made lowercase.
    c312a = models.ForeignKey(Classes, models.DO_NOTHING, db_column='C312A', related_name='classroomschedule_c312a_set',
                              blank=True, null=False)  # Field name made lowercase.
    c312b = models.ForeignKey(Classes, models.DO_NOTHING, db_column='C312B', related_name='classroomschedule_c312b_set',
                              blank=True, null=False)  # Field name made lowercase.
    c403 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='C403', related_name='classroomschedule_c403_set',
                             blank=True, null=False)  # Field name made lowercase.
    c404_lab = models.ForeignKey(Classes, models.DO_NOTHING, db_column='C404_lab',
                                 related_name='classroomschedule_c404_lab_set', blank=True,
                                 null=False)  # Field name made lowercase.
    c405_lab = models.ForeignKey(Classes, models.DO_NOTHING, db_column='C405_lab',
                                 related_name='classroomschedule_c405_lab_set', blank=True,
                                 null=False)  # Field name made lowercase.
    comp_lab = models.ForeignKey(Classes, models.DO_NOTHING, db_column='COMP_LAB',
                                 related_name='classroomschedule_comp_lab_set', blank=True,
                                 null=False)  # Field name made lowercase.
    xh105 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH105', related_name='classroomschedule_xh105_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh201 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH201', related_name='classroomschedule_xh201_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh202 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH202', related_name='classroomschedule_xh202_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh203 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH203', related_name='classroomschedule_xh203_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh204 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH204', related_name='classroomschedule_xh204_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh205 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH205', related_name='classroomschedule_xh205_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh301 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH301', related_name='classroomschedule_xh301_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh302 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH302', related_name='classroomschedule_xh302_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh303 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH303', related_name='classroomschedule_xh303_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh304 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH304', related_name='classroomschedule_xh304_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh305 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH305', related_name='classroomschedule_xh305_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh401 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH401', related_name='classroomschedule_xh401_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh402 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH402', related_name='classroomschedule_xh402_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh403 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH403', related_name='classroomschedule_xh403_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh404 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH404', related_name='classroomschedule_xh404_set',
                              blank=True, null=False)  # Field name made lowercase.
    xh405 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='XH405', related_name='classroomschedule_xh405_set',
                              blank=True, null=False)  # Field name made lowercase.
    lrc203 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='LRC203',
                               related_name='classroomschedule_lrc203_set', blank=True,
                               null=False)  # Field name made lowercase.
    lrc204 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='LRC204',
                               related_name='classroomschedule_lrc204_set', blank=True,
                               null=False)  # Field name made lowercase.
    lrc207 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='LRC207',
                               related_name='classroomschedule_lrc207_set', blank=True,
                               null=False)  # Field name made lowercase.
    lrc208 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='LRC208',
                               related_name='classroomschedule_lrc208_set', blank=True,
                               null=False)  # Field name made lowercase.
    lrc303a = models.ForeignKey(Classes, models.DO_NOTHING, db_column='LRC303A',
                                related_name='classroomschedule_lrc303a_set', blank=True,
                                null=False)  # Field name made lowercase.
    lrc305 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='LRC305',
                               related_name='classroomschedule_lrc305_set', blank=True,
                               null=False)  # Field name made lowercase.
    lrc309 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='LRC309',
                               related_name='classroomschedule_lrc309_set', blank=True,
                               null=False)  # Field name made lowercase.
    lrc311 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='LRC311',
                               related_name='classroomschedule_lrc311_set', blank=True,
                               null=False)  # Field name made lowercase.
    s301 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='S301', related_name='classroomschedule_s301_set',
                             blank=True, null=False)  # Field name made lowercase.
    s302 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='S302', related_name='classroomschedule_s302_set',
                             blank=True, null=False)  # Field name made lowercase.
    s303 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='S303', related_name='classroomschedule_s303_set',
                             blank=True, null=False)  # Field name made lowercase.
    s304 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='S304', related_name='classroomschedule_s304_set',
                             blank=True, null=False)  # Field name made lowercase.
    s305 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='S305', related_name='classroomschedule_s305_set',
                             blank=True, null=False)  # Field name made lowercase.
    s401 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='S401', related_name='classroomschedule_s401_set',
                             blank=True, null=False)  # Field name made lowercase.
    s402 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='S402', related_name='classroomschedule_s402_set',
                             blank=True, null=False)  # Field name made lowercase.
    s403 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='S403', related_name='classroomschedule_s403_set',
                             blank=True, null=False)  # Field name made lowercase.
    s404 = models.ForeignKey(Classes, models.DO_NOTHING, db_column='S404', related_name='classroomschedule_s404_set',
                             blank=True, null=False)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'classroomSchedule'


class Classrooms(models.Model):
    classroomid = models.AutoField(db_column='classroomID', primary_key=True)  # Field name made lowercase.
    roomname = models.TextField(db_column='roomName')  # Field name made lowercase.
    floor = models.IntegerField()
    capacity = models.IntegerField()
    bldg = models.TextField()
    type = models.TextField()

    class Meta:
        managed = False
        db_table = 'classrooms'


class Courses(models.Model):
    course_id = models.AutoField(db_column='course_id', primary_key=True)  # Field name made lowercase.
    code = models.TextField(unique=True)
    description = models.TextField()
    units = models.FloatField()

    class Meta:
        managed = False
        db_table = 'courses'


class Offspring(models.Model):
    timeid = models.OneToOneField('Timeslots', models.DO_NOTHING, db_column='timeID',
                                  primary_key=True)  # Field name made lowercase. The composite primary key (timeID, classroomID) found, that is not supported. The first column is selected.
    classid = models.ForeignKey(Classes, models.DO_NOTHING, db_column='classID',
                                to_field=None)  # Field name made lowercase.
    classroomid = models.ForeignKey(Classrooms, models.DO_NOTHING, db_column='classroomID',
                                    to_field=None)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'offspring'


class Programs(models.Model):
    programid = models.AutoField(db_column='programID', primary_key=True)  # Field name made lowercase.
    name = models.TextField()
    firstyears = models.IntegerField(db_column='firstYears', blank=True, null=False)  # Field name made lowercase.
    secondyears = models.IntegerField(db_column='secondYears', blank=True, null=False)  # Field name made lowercase.
    thirdyears = models.IntegerField(db_column='thirdYears', blank=True, null=False)  # Field name made lowercase.
    fourthyears = models.IntegerField(db_column='fourthYears', blank=True, null=False)  # Field name made lowercase.
    groupfirstyear = models.IntegerField(db_column='groupFirstYear', blank=True,
                                         null=False)  # Field name made lowercase.
    groupsecondyear = models.IntegerField(db_column='groupSecondYear', blank=True,
                                          null=False)  # Field name made lowercase.
    groupthirdyear = models.IntegerField(db_column='groupThirdYear', blank=True,
                                         null=False)  # Field name made lowercase.
    groupfourthyear = models.IntegerField(db_column='groupFourthYear', blank=True,
                                          null=False)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'programs'


class Prospectus(models.Model):
    prospectus_id = models.AutoField(db_column='prospectus_id', primary_key=True)  # Field name made lowercase.
    course_id = models.ForeignKey('Courses', models.DO_NOTHING, db_column='course_id',
                                 to_field=None)  # Field name made lowercase.
    program_id = models.ForeignKey(Programs, models.DO_NOTHING, db_column='program_id',
                                  to_field=None)  # Field name made lowercase.
    year = models.IntegerField()
    semester = models.IntegerField(blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'prospectus'
        unique_together = (('course_id', 'prospectus_id'),)


class Rleschedule(models.Model):
    rleid = models.AutoField(db_column='rleID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    sectionid = models.ForeignKey('Sections', models.DO_NOTHING, db_column='sectionID', to_field=None, blank=True,
                                  null=False)  # Field name made lowercase.
    timeid = models.ForeignKey('Timeslots', models.DO_NOTHING, db_column='timeID', to_field=None, blank=True,
                               null=False)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'rleSchedule'


class Sections(models.Model):
    sectionid = models.AutoField(db_column='sectionID', primary_key=True, blank=True,
                                 null=False)  # Field name made lowercase.
    programid = models.ForeignKey(Programs, models.DO_NOTHING, db_column='programID', to_field=None, blank=True,
                                  null=False)  # Field name made lowercase.
    year = models.IntegerField()
    section = models.TextField()

    class Meta:
        managed = False
        db_table = 'sections'


class Timeslots(models.Model):
    timeid = models.AutoField(db_column='timeID', primary_key=True)  # Field name made lowercase.
    timestart = models.TextField(db_column='timeStart')  # Field name made lowercase.
    timeend = models.TextField(db_column='timeEnd')  # Field name made lowercase.
    day = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'timeSlots'
