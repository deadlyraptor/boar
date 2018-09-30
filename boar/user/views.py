# views for users

import os
import secrets
from boar import app, db
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from ..models import Organization, User
from .forms import (LoginForm, OrganizationForm, RegistrationForm,
                    UpdateAccountForm)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registers a user.

    Two forms are used because users belong to an organization, which is a
    separate model.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    registration_form = RegistrationForm()
    organization_form = OrganizationForm()
    if registration_form.validate_on_submit():
        user = User(username=registration_form.username.data,
                    email=registration_form.email.data,
                    first_name=registration_form.first_name.data,
                    last_name=registration_form.last_name.data)
        user.set_password(registration_form.password.data)
        user.set_organization(organization_form.name.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.',
              'success')
        return redirect(url_for('login'))
    return render_template('/user/register.html', title='Register',
                           registration_form=registration_form,
                           organization_form=organization_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'You have logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template('/user/login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route('/account/<username>', methods=['GET', 'POST'])
@login_required
def account(username):
    """
    Renders a profile page for the user from where they can also
    their profile.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_photo = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_photo = url_for('static',
                            filename='images/' + current_user.profile_photo)
    return render_template('/user/account.html', title='Account',
                           profile_photo=profile_photo, form=form)


@app.route('/organization/<int:id>')
@login_required
def organization(id):
    """
    Renders a profile page for the user's organization.
    """
    organization = Organization.query.get_or_404(id)
    return render_template('/user/organization.html',
                           organization=organization)
