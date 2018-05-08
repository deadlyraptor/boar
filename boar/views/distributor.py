# distributor.py

from boar import app
from flask import Flask, flash, render_template, request, redirect, url_for
from ..db_setup import db_session
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
                                  city=form.city.data, state=form.state.data,
                                  zip=form.zip.data)
        db_session.add(distributor)
        db_session.commit()
        flash('Distributor added successfully!')
        return redirect(url_for('index'))
    return render_template('/distributor/new.html', form=form)


@app.route('/distributors')
def list_distributors():
    distributors = []
    qry = db_session.query(Distributor).order_by(Distributor.company)
    distributors = qry.all()

    if not distributors:
        flash('No distributors found!')
        return redirect('/')
    else:
        table = Distributors(distributors)
        table.border = True
        return render_template('/distributor/distributors.html', table=table)


@app.route('/distributor/edit/<int:id>', methods=['GET', 'POST'])
def edit_distributor(id):
    qry = db_session.query(Distributor).filter(Distributor.id == id)
    distributor = qry.first()

    if distributor:
        form = DistributorForm(formdata=request.form, obj=distributor)
        if form.validate_on_submit():
            save_distributor(distributor, form)
            flash('Distributor updated successfully!')
            return redirect('/')
        return render_template('/distributor/edit.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@app.route('/distributor/delete/<int:id>', methods=['GET', 'POST'])
def delete_distributor(id):
    """
    Delete the item in the database that matches the specified ID in the URL
    """
    qry = db_session.query(Distributor).filter(Distributor.id == id)
    distributor = qry.first()

    if distributor:
        form = DistributorForm(formdata=request.form, obj=distributor)
        if form.validate_on_submit():
            db_session.delete(distributor)
            db_session.commit()

            flash('Distributor deleted successfully!')
            return redirect('/')
        return render_template('/distributor/delete.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)
