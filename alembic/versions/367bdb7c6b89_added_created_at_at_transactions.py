"""added created at at transactions

Revision ID: 367bdb7c6b89
Revises: 386756d00ea2
Create Date: 2022-09-13 00:54:34.033548

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '367bdb7c6b89'
down_revision = '386756d00ea2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction', 'created_at')
    # ### end Alembic commands ###
