"""added item result

Revision ID: d44f8d99390b
Revises: 9fa0729592d4
Create Date: 2021-12-14 10:56:17.536960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd44f8d99390b'
down_revision = '9fa0729592d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item_result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('is_correct', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('options', sa.Column('is_correct', sa.Boolean(), nullable=True))
    op.drop_column('options', 'correct_answer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('options', sa.Column('correct_answer', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('options', 'is_correct')
    op.drop_table('item_result')
    # ### end Alembic commands ###