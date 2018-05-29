# user.py

from boar import app
from flask import flash, render_template, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from ..models import User, Organization
from ..forms import LoginForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('/forms/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    profile = User.query.join(Organization, User.organization_id ==
                              Organization.id).add_columns(
                              User.username, User.first_name, User.last_name,
                              User.email, Organization.name).filter(
                              Organization.id == 1).first_or_404()
    return render_template('/user/user.html', profile=profile)


@app.route('/organization/<id>')
@login_required
def organization(id):
    organization = Organization.query.filter_by(
        id=current_user.organization_id).first_or_404()
    return render_template('/user/organization.html',
                           organization=organization)
