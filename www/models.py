#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Lightsing'

import time, uuid

from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField

class User(Model):
    __table__ = 'user_tbl'

    id = IntegerField(primary_key=True)
    user_id = IntegerField()
    user_type = IntegerField()
    user_key = StringField(ddl='CHAR(32)')

class User(Model):
    __table__ = 'user_tbl'

    id = IntegerField(primary_key=True)
    user_id = IntegerField()
    user_type = IntegerField()
    user_key = StringField(ddl='CHAR(32)')


class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(updatable=False, ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(updatable=False, default=time.time)

class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(updatable=False, ddl='varchar(50)')
    user_id = StringField(updatable=False, ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(updatable=False, default=time.time)
