# distributor.py

from boar import app, db
from flask import flash, render_template, redirect, url_for
from flask_login import login_required
from ..models import Distributor
from ..forms import DistributorForm
from ..tables import Distributors


@app.route('/distributor/new', methods=['GET', 'POST'])
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
                                  zip=form.zip.data)
        db.session.add(distributor)
        db.session.commit()
        flash('Distributor added successfully!')
        return redirect(url_for('index'))
    return render_template('/forms/distributor.html', title='New Distributor',
                           heading='New Distributor', form=form)


@app.route('/distributors')
@login_required
def list_distributors():
    distributors = Distributor.query.order_by(Distributor.company).all()
    if not distributors:
        flash('No distributors found!')
        return redirect(url_for('index'))
    else:
        table = Distributors(distributors)
        return render_template('/distributor/distributors.html', table=table)


@app.route('/distributor/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_distributor(id):
    distributor = Distributor.query.filter(Distributor.id == id).first()
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
        return redirect(url_for('index'))
    return render_template('/forms/distributor.html', title='Edit Distributor',
                           heading='Edit Distributor', form=form)


@app.route('/distributor/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_distributor(id):
    """
    Delete the item in the database that matches the specified ID in the URL
    """
    distributor = Distributor.query.filter(Distributor.id == id).first()
    if distributor:
        form = DistributorForm(obj=distributor)
        if form.validate_on_submit():
            db.session.delete(distributor)
            db.session.commit()
            flash('Distributor deleted successfully!')
            return redirect(url_for('index'))
        return render_template('/forms/distributor.html',
                               title='Delete Distributor',
                               heading='Delete Distributor', form=form)
