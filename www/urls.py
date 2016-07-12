#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

import os, re, time, base64, hashlib, logging

from transwarp.web import get, post, ctx, view, interceptor, seeother, notfound

from apis import api, APIError, APIValueError, APIPermissionError, APIResourceNotFoundError

from models import User

def make_signed_cookie(id, password, max_age):
    # build cookie string by: id-expires-md5
    expires = str(int(time.time() + (max_age or 86400)))
    L = [id, expires, hashlib.md5('%s-%s-%s-%s' % (id, password, expires, _COOKIE_KEY)).hexdigest()]
    return '-'.join(L)

def parse_signed_cookie(cookie_str):
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        id, expires, md5 = L
        if int(expires) < time.time():
            return None
        user = User.get(id)
        if user is None:
            return None
        if md5 != hashlib.md5('%s-%s-%s-%s' % (id, user.password, expires, _COOKIE_KEY)).hexdigest():
            return None
        return user
    except:
        return None

@view('basic.html')
@get('/')
def test_users():
    users = User.find_all()
    return dict(users=users)

@view('register.html')
@get('/register')
def register():
    return dict()

_RE_ID = re.compile(r'^[0-9]{8}$')
_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')

@api
@post('/api/users')
def register_user():
    i = ctx.request.input(user_name='', user_id='', user_key='')
    re_name = i.user_name.strip()
    re_id = i.user_id.strip()
    re_key = i.user_key
    if not name:
        raise APIValueError('name')
    if not re_id or not _RE_ID.match(re_id):
        raise APIValueError('id')
    if not re_key or not _RE_MD5.match(re_key):
        raise APIValueError('password')
    user = User.find_first('where user_id=?', re_id)
    if user:
        raise APIError('register:failed', 'id', 'ID is already in use.')
    user = User(user_id=re_id, user_type=1, user_key=re_key)
    user.insert()
    # make session cookie:
    cookie = make_signed_cookie(user.user_id, user.user_key, None)
    ctx.response.set_cookie(_COOKIE_NAME, cookie)
    return user
