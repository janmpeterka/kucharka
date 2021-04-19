"""Add ingredients and recipes

Revision ID: eed4b237589f
Revises: 9973a062e3ed
Create Date: 2021-04-19 16:51:36.483312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eed4b237589f"
down_revision = "9973a062e3ed"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ingredients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("last_updated_at", sa.DateTime(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("measurement", sa.Enum("gram", "kus"), nullable=False),
        sa.Column("calorie", sa.Float(), server_default=sa.text("'0'"), nullable=False),
        sa.Column("sugar", sa.Float(), server_default=sa.text("'0'"), nullable=False),
        sa.Column("fat", sa.Float(), server_default=sa.text("'0'"), nullable=False),
        sa.Column("protein", sa.Float(), server_default=sa.text("'0'"), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ingredients_created_by"), "ingredients", ["created_by"], unique=False
    )
    op.create_table(
        "recipes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("last_updated_at", sa.DateTime(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_recipes_created_by"), "recipes", ["created_by"], unique=False
    )
    op.create_table(
        "recipes_have_ingredients",
        sa.Column("recipes_id", sa.Integer(), nullable=False),
        sa.Column("ingredients_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["ingredients_id"], ["ingredients.id"]),
        sa.ForeignKeyConstraint(["recipes_id"], ["recipes.id"]),
        sa.PrimaryKeyConstraint("recipes_id", "ingredients_id"),
    )
    op.create_index(
        op.f("ix_recipes_have_ingredients_ingredients_id"),
        "recipes_have_ingredients",
        ["ingredients_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_recipes_have_ingredients_recipes_id"),
        "recipes_have_ingredients",
        ["recipes_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_index(
    #     op.f("ix_recipes_have_ingredients_recipes_id"),
    #     table_name="recipes_have_ingredients",
    # )
    # op.drop_index(
    #     op.f("ix_recipes_have_ingredients_ingredients_id"),
    #     table_name="recipes_have_ingredients",
    # )
    op.drop_table("recipes_have_ingredients")
    # op.drop_index(op.f("ix_recipes_created_by"), table_name="recipes")
    op.drop_table("recipes")
    # op.drop_index(op.f("ix_ingredients_created_by"), table_name="ingredients")
    op.drop_table("ingredients")
    # ### end Alembic commands ###
