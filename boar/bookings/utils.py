from flask_login import current_user
from ..models import Distributor, Program


def query_distributor():
    distributor = Distributor.query.order_by(Distributor.company).filter_by(
        organization_id=current_user.organization_id)
    return distributor


def query_program():
    distributor = Program.query.order_by(Program.name).filter_by(
        organization_id=current_user.organization_id, active=1)
    return distributor
