from flask_login import current_user
from ..models import Distributor, Program


def query_distributor():
    distributor = Distributor.query.order_by(Distributor.company).filter(
        Distributor.organization_id == current_user.organization_id)
    return distributor


def query_program():
    distributor = Program.query.order_by(Program.name).filter(
        Program.organization_id == current_user.organization_id,
        Program.active == 1)
    return distributor
