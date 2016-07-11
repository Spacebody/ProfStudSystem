#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

import logging

from transwarp.web import get, view

from models import User

@view('basic.html')
@get('/')
def test_users():
    users = User.find_all()
    return dict(users=users)
