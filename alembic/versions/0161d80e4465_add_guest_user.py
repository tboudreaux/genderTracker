"""Add Guest User

Revision ID: 0161d80e4465
Revises: 4d7ea175f82b
Create Date: 2023-11-27 12:37:40.074835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0161d80e4465'
down_revision: Union[str, None] = '4d7ea175f82b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('days', sa.Column('datetime', sa.DateTime(timezone=True), nullable=False))
    op.drop_column('days', 'date')

    conn = op.get_bind()
    metadata = sa.MetaData()

    User = sa.Table('users', metadata, autoload_with=conn)
    query = User.select().where(User.c.username == 'guest')
    result = conn.execute(query)

    if result.rowcount == 0:
        conn.execute(
            User.insert().values(
                uuid="00000000-0000-0000-0000-000000000000",
                username='guest',
                password='guest',
                email="guest@example.com",
                salt="qqq",
                created_at=sa.func.now(),
            ))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('days', sa.Column('date', sa.DATE(), autoincrement=False, nullable=False))
    op.drop_column('days', 'datetime')
    # ### end Alembic commands ###
