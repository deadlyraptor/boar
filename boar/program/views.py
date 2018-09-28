# views for programs

from boar import app, db
from flask import flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Program
from .forms import ProgramForm
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
    return render_template('/programs/new_program.html', form=form,
                           title='New Program', heading='New Program')


@app.route('/programs', methods=['GET', 'POST'])
@login_required
def view_programs():
    """
    Displays a table with all active programs.
    """
    programs = Program.query.order_by(Program.name).filter(
        Program.organization_id == current_user.organization_id).all()
        # Program.active == 1).all()
    if not programs:
        flash('No programs found!')
        return redirect(url_for('index'))
    else:
        table = Programs(programs)
        return render_template('/programs/programs.html',
                               table=table, title='Programs',
                               heading='Programs', programs=programs)


@app.route('/programs/<int:id>', methods=['GET', 'POST'])
@login_required
def deactivate(id):
    program = Program.query.filter(Program.id == id).first_or_404()
    program.active = 0
    db.session.commit()
    flash('Program successfully deactived.')
    return redirect(url_for('view_programs'))
