"""make description nullable in documents

Revision ID: 94ade53bd051
Revises: 368258255e0b
Create Date: 2026-09-06 10:43:08.593030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94ade53bd051'
down_revision: Union[str, Sequence[str], None] = '368258255e0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.alter_column('documents', 'description',
               existing_type=sa.Text(),
               nullable=True)


def downgrade() -> None:
   
    op.alter_column('documents', 'description',
               existing_type=sa.Text(),
               nullable=False)
