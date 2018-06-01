# program.py

from boar import app, db
from flask import flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Program
from ..forms import ProgramForm
from ..tables import Programs


@app.route('/program/new', methods=['GET', 'POST'])
@login_required
def new_program():
    """
    Add a new program
    """
    form = ProgramForm()
    if form.validate_on_submit():
        program = Program(name=form.name.data,
                          organization_id=current_user.organization_id)
        db.session.add(program)
        db.session.commit()
        flash('Program added successfully!')
        return redirect(url_for('index'))
    return render_template('/forms/program.html', title='New Program',
                           heading='New Program', form=form)


@app.route('/programs', methods=['GET', 'POST'])
@login_required
def view_programs():
    programs = Program.query.order_by(Program.name).filter(
        Program.organization_id == current_user.organization_id).all()
    if not programs:
        flash('No programs found!')
        return redirect(url_for('index'))
    else:
        table = Programs(programs)
        return render_template('/program/view.html', table=table)
