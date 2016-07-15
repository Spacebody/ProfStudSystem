#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

import os, re, time, base64, hashlib, logging

from transwarp.web import get, post, ctx, view, interceptor, seeother, notfound

from apis import api, APIError, APIValueError, APIPermissionError, APIResourceNotFoundError

from models import User, Student, Professor

from config import configs

_COOKIE_NAME = 'sustc_profstdu'
_COOKIE_KEY = configs.session.secret

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
        user_id, expires, md5 = L
        if int(expires) < time.time():
            return None
        user = User.find_first('where user_id=?', user_id)
        if user is None:
            return None
        if md5 != hashlib.md5('%s-%s-%s-%s' % (user_id, user.user_key, expires, _COOKIE_KEY)).hexdigest():
            return None
        return user
    except:
        return None

@interceptor('/')
def user_interceptor(next):
    logging.info('try to bind user from session cookie...')
    user = None
    cookie = ctx.request.cookies.get(_COOKIE_NAME)
    if cookie:
        logging.info('parse session cookie...')
        user = parse_signed_cookie(cookie)
        if user:
            logging.info('bind user <%s> to session...' % user.user_id)
    ctx.request.user = user
    return next()

@view('index.html')
@get('/')
def index():
    student = None
    user = ctx.request.user
    if user:
        user.user_key = '******'
    if ctx.request.user:
        student = Student.find_first('where stdu_id=?', ctx.request.user.user_id)
    return dict(user=user, stdu = student)

@view('signin.html')
@get('/signin')
def signin():
    if ctx.request.user:
        raise seeother('/')
    return dict()

@get('/signout')
def signout():
    ctx.response.delete_cookie(_COOKIE_NAME)
    raise seeother('/')

@interceptor('/manage/')
def manage_interceptor(next):
    user = ctx.request.user
    if user and user.admin:
        return next()
    raise seeother('/signin')

@view('register.html')
@get('/register')
def register():
    return dict()

@api
@post('/api/authenticate')
def authenticate():
    i = ctx.request.input(remember='')
    user_id = i.re_id.strip()
    user_key = i.re_key
    remember = i.remember
    user = User.find_first('where user_id=?', user_id)
    if user is None:
        raise APIError('auth:failed', 'email', 'Invalid email.')
    elif user.user_key != user_key:
        raise APIError('auth:failed', 'password', 'Invalid password.')
    # make session cookie:
    max_age = 604800 if remember=='true' else None
    cookie = make_signed_cookie(str(user.user_id), user.user_key, max_age)
    ctx.response.set_cookie(_COOKIE_NAME, cookie, max_age=max_age)
    user.user_key = '******'
    return user

_RE_ID = re.compile(r'^[0-9]{8}$')
_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')

@api
@post('/api/users')
def register_user():
    i = ctx.request.input(user_name='', user_id='', user_key='')
    re_name = i.user_name.strip()
    re_id = i.user_id.strip()
    re_key = i.user_key
    if not re_name:
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
    cookie = make_signed_cookie(str(user.user_id), user.user_key, None)
    ctx.response.set_cookie(_COOKIE_NAME, cookie)
    return user
