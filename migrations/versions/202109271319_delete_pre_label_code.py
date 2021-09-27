"""Delete pre-label code

Revision ID: 6f81e793e8e6
Revises: 85fc374dd038
Create Date: 2021-09-27 13:19:19.645302

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "6f81e793e8e6"
down_revision = "85fc374dd038"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("ingredients", "gluten_free")
    op.drop_column("ingredients", "lactose_free")
    op.drop_column("ingredients", "is_vegan")
    op.drop_column("ingredients", "is_vegetarian")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "ingredients",
        sa.Column(
            "is_vegetarian",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "ingredients",
        sa.Column(
            "is_vegan",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "ingredients",
        sa.Column(
            "lactose_free",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "ingredients",
        sa.Column(
            "gluten_free",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=True,
        ),
    )
    # ### end Alembic commands ###
