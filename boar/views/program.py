# program.py

from boar import app, db
from flask import Flask, flash, render_template, redirect, url_for
from ..models import Program
from ..forms import ProgramForm
from ..tables import Programs


@app.route('/program/new', methods=['GET', 'POST'])
def new_program():
    """
    Add a new program
    """
    form = ProgramForm()
    if form.validate_on_submit():
        program = Program(name=form.name.data)
        db.session.add(program)
        db.session.commit()
        flash('Program added successfully!')
        return redirect(url_for('index'))
    return render_template('/program/new.html', form=form)


@app.route('/programs', methods=['GET', 'POST'])
def view_programs():
    programs = Program.query.order_by(Program.name).all()
    if not programs:
        flash('No programs found!')
        return redirect(url_for('index'))
    else:
        table = Programs(programs)
        table.border = True
        return render_template('/program/view.html', table=table)
