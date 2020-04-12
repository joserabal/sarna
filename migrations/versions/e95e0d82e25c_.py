"""empty message

Revision ID: e95e0d82e25c
Revises: 8abb844b1c27
Create Date: 2020-04-09 17:30:49.872984

"""
from alembic import op
import sqlalchemy as sa
import sarna


# revision identifiers, used by Alembic.
revision = 'e95e0d82e25c'
down_revision = '8abb844b1c27'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('template')

    op.create_table(
        'template',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=32), nullable=False),
        sa.Column('description', sa.String(length=128), nullable=False),
        sa.Column('last_modified', sa.DateTime(), nullable=False),
        sa.Column('file', sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'client_template',
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['client.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['template_id'], ['template.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('client_id', 'template_id')
    )

    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('client_template')
    op.drop_table('template')

    op.create_table('template',
        sa.Column('name', sa.String(length=32), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(length=128), nullable=True),
        sa.Column('file', sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['client.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('name', 'client_id')
    )
    # ### end Alembic commands ###
