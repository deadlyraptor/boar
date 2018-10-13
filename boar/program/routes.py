# routes for programs

from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Program
from .forms import ProgramForm
from boar import db

programs_bp = Blueprint('programs_bp', __name__)


@programs_bp.route('/program/new', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    return render_template('/programs/new_program.html', form=form,
                           title='New Program', heading='New Program')


@programs_bp.route('/programs', methods=['GET', 'POST'])
@login_required
def view_programs():
    """
    Displays a table with all active programs.
    """
    programs = Program.query.order_by(Program.name).filter_by(
        organization_id=current_user.organization_id).all()
    if not programs:
        flash('No programs found.', 'warning')
        return redirect(url_for('main.index'))
    else:
        return render_template('/programs/programs.html',
                               programs=programs, title='Programs',
                               heading='Programs')


@programs_bp.route('/programs/<int:id>', methods=['GET', 'POST'])
@login_required
def deactivate(id):
    program = Program.query.filter_by(id=id).first_or_404()
    program.active = 0
    db.session.commit()
    flash('Program successfully deactived.', 'success')
    return redirect(url_for('programs_bp.view_programs'))
