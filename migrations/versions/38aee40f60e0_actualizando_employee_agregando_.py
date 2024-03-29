"""actualizando employee agregando contraseña

Revision ID: 38aee40f60e0
Revises: ed5d67dbe37a
Create Date: 2023-10-12 18:53:59.953452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38aee40f60e0'
down_revision = 'ed5d67dbe37a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###
