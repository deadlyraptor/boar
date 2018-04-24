# distributor.py

from boar import app
from flask import Flask, flash, render_template, request, redirect
from .db_setup import db_session
from .models import Distributor
from .forms import DistributorForm
from .tables import Distributors


@app.route('/new', methods=['GET', 'POST'])
def new_distributor():
    """
    Add a new distributor
    """
    form = DistributorForm(request.form)

    if request.method == 'POST' and form.validate():
        distributor = Distributor()
        save_distributor(distributor, form, new=True)
        flash('Distributor added successfully!')
        return redirect('/')

    return render_template('/distributor/new.html', form=form)


def save_distributor(distributor, form, new=False):
    """
    Save the changes to the database
    """
    # get the data from form and assign it to the correct attributes of the
    # SQLAlchemy table object

    distributor.company = form.company.data
    distributor.payee = form.payee.data
    distributor.address1 = form.address1.data
    distributor.address2 = form.address2.data
    distributor.city = form.city.data
    distributor.state = form.state.data
    distributor.zip = form.zip.data

    if new:
        db_session.add(distributor)

    db_session.commit()


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


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Distributor).filter(Distributor.id == id)
    distributor = qry.first()

    if distributor:
        form = DistributorForm(formdata=request.form, obj=distributor)
        if request.method == 'POST' and form.validate():
            save_distributor(distributor, form)
            flash('Distributor updated successfully!')
            return redirect('/')
        return render_template('/distributor/edit.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_distributor(id):
    """
    Delete the item in the database that matches the specified ID in the URL
    """
    qry = db_session.query(Distributor).filter(Distributor.id == id)
    distributor = qry.first()

    if distributor:
        form = DistributorForm(formdata=request.form, obj=distributor)
        if request.method == 'POST' and form.validate():
            db_session.delete(distributor)
            db_session.commit()

            flash('Distributor deleted successfully!')
            return redirect('/')
        return render_template('/distributor/delete.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)
