#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Lightsing'

import time, uuid

from transwarp.db import next_id
from transwarp.orm import Model, IntegerField, StringField, FloatField

class User(Model):
    __table__ = 'user_tbl'

    id = IntegerField(primary_key=True)
    user_id = IntegerField()
    user_type = IntegerField()
    user_key = StringField(ddl='char(32)')

class Student(Model):
    __table__ = 'stdu_tbl'

    stdu_id = IntegerField(primary_key=True)
    stdu_name = StringField(ddl='varchar(10)')
    stdu_grade = IntegerField()
    stdu_college = IntegerField()
    stdu_gender = IntegerField()

class Professor(Model):
    __table__ = 'prof_tbl'

    prof_id = IntegerField(primary_key=True)
    prof_dept = IntegerField()
    prof_college = IntegerField()
    prof_photo = StringField(ddl='varchar(40)')
    prof_desc = StringField(ddl='varchar(1000)')
    max_std = IntegerField()
    std_num = IntegerField()

class Department(Model):
    __table__ = 'dept_tbl'

    dept_id = IntegerField(primary_key=True)
    dept_name = StringField(ddl='varchar(40)')

class College(Model):
    __table__ = 'college_tbl'

    college_id = IntegerField(primary_key=True)
    college_name = StringField(ddl='varchar(40)')

class Association(Model):
    __table__ = 'assoc_tbl'

    id = IntegerField(primary_key=True)
    prof_id = IntegerField()
    stdu_id = IntegerField()

class Application(Model):
    __table__ = 'apply_tbl'

    id = IntegerField(primary_key=True)
    stdu_id = IntegerField()
    prof_id1 = IntegerField()
    prof_id2 = IntegerField()
    discription = StringField(ddl='varchar(400)')

class Task(Model):
    __table__ = 'task_tbl'

    id = IntegerField(primary_key=True)
    college_id = IntegerField()
    stdu_due_time = FloatField(updatable=False)
    prof_due_time = FloatField(updatable=False)
