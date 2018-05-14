"""programs table

Revision ID: d631893d2f90
Revises: 5dab81d94ebc
Create Date: 2018-05-13 18:30:46.615457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd631893d2f90'
down_revision = '5dab81d94ebc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('programs',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('organization_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['organization_id'],
                                            ['organizations.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('program_id',
                                      sa.Integer(), nullable=True))
        batch_op.create_foreign_key('program_id', 'programs',
                                    ['program_id'], ['id'])
        batch_op.drop_column('program')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('program', sa.VARCHAR(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('program_id')

    op.drop_table('programs')
    # ### end Alembic commands ###
