# views for users

from boar import app
from flask import flash, redirect, render_template, request, url_for
from werkzeug.urls import url_parse
from flask_login import current_user, login_required, login_user, logout_user
from ..models import Organization, User
from .forms import LoginForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        else:
            flash(f'You have logged in!', 'success')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('/user/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    profile = User.query.join(Organization,
                              current_user.organization_id == Organization.id
                              ).add_columns(
                              User.username, User.first_name, User.last_name,
                              User.email, Organization.name).filter(
                              User.id == current_user.id).first_or_404()
    return render_template('/user/profile.html', profile=profile)


@app.route('/organization/<id>')
@login_required
def organization(id):
    """
    Renders a page with the user's organization.
    """
    organization = Organization.query.filter_by(
        id=current_user.organization_id).first_or_404()
    return render_template('/user/organization.html',
                           organization=organization)
