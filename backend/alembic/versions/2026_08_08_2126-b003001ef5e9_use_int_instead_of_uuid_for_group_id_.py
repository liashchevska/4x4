"""Use int instead of uuid for Group.id and Word.id

Revision ID: b003001ef5e9
Revises: bc7b11b62a11
Create Date: 2026-08-08 21:26:44.576104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b003001ef5e9'
down_revision: Union[str, Sequence[str], None] = 'bc7b11b62a11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Drop fk & pk constraints
    op.drop_constraint("words_group_id_fkey", "words", type_="foreignkey")
    op.drop_constraint("words_pkey", "words", type_="primary")
    op.drop_constraint("groups_pkey", "groups", type_="primary")

    # Create temporary int columns for pks & fk
    op.add_column("groups", sa.Column("temp_id", sa.Integer(), nullable=True))
    op.add_column("words", sa.Column("temp_id", sa.Integer(), nullable=True))
    op.add_column("words", sa.Column("temp_group_id", sa.Integer(), nullable=True))

    # Create sequences for new int ids
    op.execute(sa.schema.CreateSequence(sa.Sequence("groups_int_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("words_int_id_seq")))

    # Populate new pks, map fk to the new group.id
    op.execute("UPDATE groups SET temp_id = nextval('groups_int_id_seq')")
    op.execute("UPDATE words SET temp_id = nextval('words_int_id_seq')")
    op.execute(
        "UPDATE words SET temp_group_id = groups.temp_id FROM groups WHERE words.group_id = groups.id "
    )

    # Make new columns non-nullable
    op.alter_column("groups", "temp_id", nullable=False)
    op.alter_column("words", "temp_id", nullable=False)
    op.alter_column("words", "temp_group_id", nullable=False)

    # Drop previous id columns
    op.drop_column("words", "id")
    op.drop_column("words", "group_id")
    op.drop_column("groups", "id")

    # Rename temp columns
    op.alter_column("words", "temp_id", new_column_name="id")
    op.alter_column("words", "temp_group_id", new_column_name="group_id")
    op.alter_column("groups", "temp_id", new_column_name="id")

    # Recreate pk & fk constraints
    op.create_primary_key("words_pkey", "words", ["id"])
    op.create_primary_key("groups_pkey", "groups", ["id"])
    op.create_foreign_key("words_group_id_fkey", "words", "groups", ["group_id"], ["id"])

    # Set sequences as defaults for autoincrementing ids
    op.alter_column("groups", "id", server_default=sa.text("nextval('groups_int_id_seq')"))
    op.alter_column("words", "id", server_default=sa.text("nextval('words_int_id_seq')"))

    # Tie sequence ownership to the columns
    op.execute("ALTER SEQUENCE groups_int_id_seq OWNED BY groups.id")
    op.execute("ALTER SEQUENCE words_int_id_seq OWNED BY words.id")


def downgrade() -> None:
    """Downgrade schema."""
    raise NotImplementedError(
        "Downgrade is not supported: new integer IDs were generated without preserving the original UUID IDs."
    )
