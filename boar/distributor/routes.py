# routes for distributors

from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Distributor
from .forms import DistributorForm
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
        flash('Distributor added successfully.', 'success')
        return redirect(url_for('distributors_bp.list_distributors'))
    return render_template('/distributors/new_distributor.html', form=form,
                           title='New Distributor', heading='New Distributor')


@distributors_bp.route('/distributor/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_distributor(id):
    """
    Updates a distributor
    """
    distributor = Distributor.query.filter_by(
        id=id, organization_id=current_user.organization_id).first_or_404()
    form = DistributorForm(obj=distributor)
    if form.validate_on_submit():
        form.populate_obj(distributor)
        db.session.commit()
        flash('Distributor successfully updated.', 'success')
        return redirect(url_for('main.index'))
    return render_template('/distributors/new_distributor.html', form=form,
                           title='Edit Distributor',
                           heading='Edit Distributor')


@distributors_bp.route('/distributor/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_distributor(id):
    """
    Deletes a distributor
    """
    distributor = Distributor.query.filter_by(id=id).first()
    db.session.delete(distributor)
    db.session.commit()
    flash('Distributor successfully deleted.', 'success')
    return redirect(url_for('distributors_bp.list_distributors'))


@distributors_bp.route('/distributors')
@login_required
def list_distributors():
    distributors = Distributor.query.order_by(Distributor.company).filter_by(
         organization_id=current_user.organization_id).all()
    if not distributors:
        flash('No distributors found.', 'warning')
        return redirect(url_for('main.index'))
    else:
        return render_template('/distributors/distributor_table.html',
                               distributors=distributors, title='Distributors',
                               heading='Distributors')
