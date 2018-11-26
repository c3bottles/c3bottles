"""initial migration

Revision ID: 995d0aeda211
Revises: 
Create Date: 2018-11-24 00:44:55.926212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '995d0aeda211'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('drop_point',
    sa.Column('number', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('removed', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('number')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.Column('token', sa.String(length=128), nullable=False),
    sa.Column('can_visit', sa.Boolean(), nullable=False),
    sa.Column('can_edit', sa.Boolean(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('must_reset_pw', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('location',
    sa.Column('loc_id', sa.Integer(), nullable=False),
    sa.Column('dp_id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lng', sa.Float(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dp_id'], ['drop_point.number'], ),
    sa.PrimaryKeyConstraint('loc_id')
    )
    op.create_table('report',
    sa.Column('rep_id', sa.Integer(), nullable=False),
    sa.Column('dp_id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('state', sa.Enum('DEFAULT', 'NEW', 'NO_CRATES', 'SOME_BOTTLES', 'REASONABLY_FULL', 'FULL', 'OVERFLOW', 'EMPTY', name='report_states'), nullable=True),
    sa.ForeignKeyConstraint(['dp_id'], ['drop_point.number'], ),
    sa.PrimaryKeyConstraint('rep_id')
    )
    op.create_table('visit',
    sa.Column('vis_id', sa.Integer(), nullable=False),
    sa.Column('dp_id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('action', sa.Enum('EMPTIED', 'ADDED_CRATE', 'REMOVED_CRATE', 'RELOCATED', 'REMOVED', 'NO_ACTION', name='visit_actions'), nullable=True),
    sa.ForeignKeyConstraint(['dp_id'], ['drop_point.number'], ),
    sa.PrimaryKeyConstraint('vis_id')
    )


def downgrade():
    op.drop_table('visit')
    op.drop_table('report')
    op.drop_table('location')
    op.drop_table('user')
    op.drop_table('drop_point')
