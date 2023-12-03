"""change primary key on days table

Revision ID: 9e7eb72ff251
Revises: 88e9200c1b49
Create Date: 2023-12-03 09:20:14.626423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
# Import the UUID type from the PostgreSQL dialect
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '9e7eb72ff251'
down_revision: Union[str, None] = '88e9200c1b49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # First drop the old primary key constraint
    op.drop_constraint('days_pkey', 'days', type_='primary')
    # Then add a new primary key constraint
    op.create_primary_key(None, 'days', ['uuid'])


def downgrade() -> None:
   # To downgrade, drop the new primary key constraint
    op.drop_constraint('days_pkey', 'days', type_='primary')
    # Recreate the composite primary key
    op.create_primary_key(None, 'days', ['user_uuid', 'gender_uuid'])

