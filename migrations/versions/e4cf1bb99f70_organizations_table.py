"""organizations table

Revision ID: e4cf1bb99f70
Revises:
Create Date: 2018-05-08 18:41:05.633205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4cf1bb99f70'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organizations',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('address1', sa.String(), nullable=True),
                    sa.Column('address2', sa.String(), nullable=True),
                    sa.Column('city', sa.String(), nullable=True),
                    sa.Column('state', sa.String(), nullable=True),
                    sa.Column('zip', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('organizations')
    # ### end Alembic commands ###
