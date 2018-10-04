# routes for distributors

from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Distributor
from .forms import DistributorForm
from ..tables import Distributors
from boar import db

distributors_bp = Blueprint('distributors_bp', __name__)


@distributors_bp.route('/distributor/new', methods=['GET', 'POST'])
@login_required
def new_distributor():
    """
    Add a new distributor
    """
    form = DistributorForm()
    if form.validate_on_submit():
        distributor = Distributor(company=form.company.data,
                                  payee=form.payee.data,
                                  address1=form.address1.data,
                                  address2=form.address2.data,
                                  city=form.city.data,
                                  state=form.state.data,
                                  zip=form.zip.data,
                                  organization_id=current_user.organization_id)
        db.session.add(distributor)
        db.session.commit()
        flash('Distributor added successfully!')
        return redirect(url_for('main.index'))
    return render_template('/distributor/distributor.html', form=form,
                           title='New Distributor', heading='New Distributor')


@distributors_bp.route('/distributors')
@login_required
def list_distributors():
    distributors = Distributor.query.order_by(Distributor.company).filter(
         Distributor.organization_id == current_user.organization_id).all()
    if not distributors:
        flash('No distributors found!')
        return redirect(url_for('main.index'))
    else:
        table = Distributors(distributors)
        return render_template('/distributor/distributor_table.html',
                               table=table, title='Distributors',
                               heading='Distributors',
                               distributors=distributors)


@distributors_bp.route('/distributor/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_distributor(id):
    distributor = Distributor.query.filter(
        Distributor.id == id,
        Distributor.organization_id == current_user.organization_id).first()
    form = DistributorForm(obj=distributor)
    if form.validate_on_submit():
        distributor.company = form.company.data
        distributor.payee = form.payee.data
        distributor.address1 = form.address1.data
        distributor.address2 = form.address2.data
        distributor.city = form.city.data
        distributor.state = form.state.data
        distributor.zip = form.zip.data
        db.session.commit()
        flash('Distributor updated successfully!')
        return redirect(url_for('main.index'))
    return render_template('/distributor/distributor.html', form=form,
                           title='Edit Distributor',
                           heading='Edit Distributor')


@distributors_bp.route('/distributor/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_distributor(id):
    """
    Delete the item in the database that matches the specified ID in the URL
    """
    distributor = Distributor.query.filter(Distributor.id == id).first()
    db.session.delete(distributor)
    db.session.commit()
    flash('Distributor successfully deleted!')
    return redirect(url_for('list_distributors'))
