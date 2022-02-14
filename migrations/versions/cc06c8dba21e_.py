"""empty message

Revision ID: cc06c8dba21e
Revises: dcd027edc639
Create Date: 2022-02-13 18:23:46.863087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc06c8dba21e'
down_revision = 'dcd027edc639'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bot_view_multi_post_order_types', sa.Column('post_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bot_view_multi_post_order_types', 'post_count')
    # ### end Alembic commands ###
