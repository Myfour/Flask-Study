"""empty message

Revision ID: ab6b5346a75d
Revises: 72d126e81103
Create Date: 2019-10-23 10:53:08.387229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab6b5346a75d'
down_revision = '72d126e81103'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cat',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('a_name', sa.String(length=16), nullable=True),
    sa.Column('c_eat', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dog',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('a_name', sa.String(length=16), nullable=True),
    sa.Column('d_legs', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dog')
    op.drop_table('cat')
    # ### end Alembic commands ###