#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import Student

from transwarp import db

db.create_engine(user='develop_root', host='10.20.2.113', password='PythonDatabase', database='develop')

s = Student(stdu_id=1151000, stdu_grade=15, stdu_college=1, stdu_gender=1)
s.insert()

s = Student(stdu_id=1151001, stdu_grade=15, stdu_college=1, stdu_gender=2)
s.insert()
