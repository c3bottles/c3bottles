"""add drop point categories

Revision ID: 7396aea8eb0a
Revises: 995d0aeda211
Create Date: 2018-11-25 18:25:33.900370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7396aea8eb0a'
down_revision = '995d0aeda211'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('drop_point', sa.Column('category_id', sa.Integer()))
    op.execute('UPDATE drop_point SET category_id = 1;')
    op.alter_column('drop_point', 'category_id', existing_type=sa.Integer(), nullable=False)


def downgrade():
    op.drop_column('drop_point', 'category_id')
