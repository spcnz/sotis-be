"""empty message

Revision ID: 7e060c8add4b
Revises: 8ebfb1869062
Create Date: 2021-12-28 14:07:25.416354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e060c8add4b'
down_revision = '8ebfb1869062'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sections_related')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sections_related',
    sa.Column('section_from', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('section_to', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['section_from'], ['sections.id'], name='sections_related_section_from_fkey'),
    sa.ForeignKeyConstraint(['section_to'], ['sections.id'], name='sections_related_section_to_fkey')
    )
    # ### end Alembic commands ###