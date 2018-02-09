# !/usr/bin/python
# coding=utf-8
from flask import render_template, url_for, flash
from flask import request, redirect
from flask_login import login_user, logout_user, current_user
from . import auth
from ..models import login_gm, UserManager, is_already_login
from .forms import LoginForm
import logging
import datetime


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 如果已经登录过,先做清理, 保证和gm server的连接有效
        if is_already_login(form.username.data, form.password.data):
            current_user.connect_gm.close()
            UserManager.remove(current_user.id)
            logging.debug('the connection of user {} to gm server already exits remove it current user id {}'.format(
                form.username.data, current_user.id))

        # 重新登录
        status_code, ret = login_gm(form.username.data, form.password.data)
        if not status_code:
            UserManager.append(ret)
            login_user(ret)
            UserManager.print_users()
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('login gm server failed {0}:{1}'.format(status_code, ret), 'error')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logging.info('user {0} logout close connect gm socket_id: {1}'.format(current_user.id,
                                                                          current_user.connect_gm.sock_id))
    current_user.connect_gm.close()
    UserManager.remove(current_user.id)
    logout_user()
    UserManager.print_users()
    flash('You have been logged out!')
    return redirect(url_for('auth.login'))


# 程序可以决定用户确认账户之前可以做什么操作，允许未确认账户登录，但是只显示一个页面，要求用户在获取权限之前先确认账户
# 使用before_request 钩子完成 before_request钩子只能应用于属于蓝本的请求上；
# 全局钩子，必须使用before_app_request修饰器

@auth.before_app_request
def before_request():
    return
