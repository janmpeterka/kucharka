"""Make ingredient loggable

Revision ID: c75bde5e945b
Revises: a334a3a614a7
Create Date: 2023-06-28 17:39:22.860818

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "c75bde5e945b"
down_revision = "a334a3a614a7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("ingredients", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
        )
        batch_op.add_column(sa.Column("updated_by", sa.Integer(), nullable=True))
        batch_op.alter_column(
            "created_at", existing_type=mysql.DATETIME(), nullable=False
        )
        batch_op.create_foreign_key(
            batch_op.f("fk_ingredients_updated_by_users"),
            "users",
            ["updated_by"],
            ["id"],
        )

    from app.models import Ingredient

    for i in Ingredient.load_all():
        i.updated_at = i.last_updated_at
        i.edit()

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("ingredients", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_ingredients_updated_by_users"), type_="foreignkey"
        )
        batch_op.alter_column(
            "created_at",
            existing_type=mysql.DATETIME(),
            nullable=True,
            server_default=sa.func.current_timestamp(),
        )
        batch_op.drop_column("updated_by")
        batch_op.drop_column("updated_at")

    # ### end Alembic commands ###
