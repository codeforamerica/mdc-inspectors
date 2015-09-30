"""empty message

Revision ID: 5411a86bfc6
Revises: None
Create Date: 2015-09-28 15:50:06.667183

"""

# revision identifiers, used by Alembic.
revision = '5411a86bfc6'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('supervisor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('last_report', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_supervisor_id'), 'supervisor', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('permit_number', sa.String(length=25), nullable=False),
    sa.Column('date_registered', sa.DateTime(), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=True),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_permit_number'), 'user', ['permit_number'], unique=False)
    op.create_table('inspector',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inspector_id', sa.String(length=25), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=False),
    sa.Column('photo_url', sa.String(length=80), nullable=True),
    sa.Column('supervisor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['supervisor_id'], ['supervisor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inspector_id'), 'inspector', ['id'], unique=False)
    op.create_index(op.f('ix_inspector_inspector_id'), 'inspector', ['inspector_id'], unique=True)
    op.create_table('inspections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('permit_number', sa.String(length=25), nullable=False),
    sa.Column('date_inspected', sa.DateTime(), nullable=False),
    sa.Column('permit_type', sa.String(length=10), nullable=False),
    sa.Column('permit_description', sa.String(length=50), nullable=True),
    sa.Column('display_description', sa.String(length=50), nullable=False),
    sa.Column('job_site_addresss', sa.String(length=200), nullable=False),
    sa.Column('inspector_id', sa.Integer(), nullable=False),
    sa.Column('feedback_form', sa.String(length=100), nullable=True),
    sa.Column('feedback_form_sent', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['inspector_id'], ['inspector.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inspections_date_inspected'), 'inspections', ['date_inspected'], unique=False)
    op.create_index(op.f('ix_inspections_id'), 'inspections', ['id'], unique=False)
    op.create_index(op.f('ix_inspections_permit_number'), 'inspections', ['permit_number'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_inspections_permit_number'), table_name='inspections')
    op.drop_index(op.f('ix_inspections_id'), table_name='inspections')
    op.drop_index(op.f('ix_inspections_date_inspected'), table_name='inspections')
    op.drop_table('inspections')
    op.drop_index(op.f('ix_inspector_inspector_id'), table_name='inspector')
    op.drop_index(op.f('ix_inspector_id'), table_name='inspector')
    op.drop_table('inspector')
    op.drop_index(op.f('ix_user_permit_number'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_supervisor_id'), table_name='supervisor')
    op.drop_table('supervisor')
    ### end Alembic commands ###
