# distributor.py

from boar import app, db
from flask import Flask, flash, render_template, redirect, url_for
from ..models import Distributor
from ..forms import DistributorForm
from ..tables import Distributors


@app.route('/distributor/new', methods=['GET', 'POST'])
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
    return render_template('/distributor/new.html', form=form)


@app.route('/distributors')
def list_distributors():
    distributors = Distributor.query.order_by(Distributor.company).all()
    if not distributors:
        flash('No distributors found!')
        return redirect(url_for('index'))
    else:
        table = Distributors(distributors)
        table.border = True
        return render_template('/distributor/distributors.html', table=table)


@app.route('/distributor/edit/<int:id>', methods=['GET', 'POST'])
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
        # save_distributor(distributor, form)
        flash('Distributor updated successfully!')
        return redirect(url_for('index'))
    return render_template('/distributor/edit.html', form=form)


@app.route('/distributor/delete/<int:id>', methods=['GET', 'POST'])
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
        return render_template('/distributor/delete.html', form=form)
