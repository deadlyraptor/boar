# routes for users

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from boar import db
from ..models import Organization, User
from .forms import (LoginForm, OrganizationForm, RegistrationForm,
                    RequestResetForm, ResetPasswordForm, UpdateAccountForm)
from boar.user.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registers a user.

    Two forms are used because users belong to an organization, which is a
    separate model.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
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
        return redirect(url_for('users.login'))
    return render_template('/user/register.html', title='Register',
                           registration_form=registration_form,
                           organization_form=organization_form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'You have logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('users.login'))
    return render_template('/user/login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/user/<username>', methods=['GET', 'POST'])
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


@users.route('/organization/<int:id>')
@login_required
def organization(id):
    """
    Renders a profile page for the user's organization.
    """
    organization = Organization.query.get_or_404(id)
    return render_template('/user/organization.html',
                           organization=organization)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to\
              reset your password.', 'info')
    return render_template('/user/reset_request.html', title='Reset Password',
                           form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.',
              'success')
        return redirect(url_for('login'))
    return render_template('/user/reset_token.html', title='Rset Password',
                           form=form)
