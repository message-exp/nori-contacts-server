import asyncpg

from models import ContactCard


async def insert_contact_card(
    conn: asyncpg.Connection,
    owner_matrix_id: str,
    contact_name: str,
    contact_avatar_url: str | None = None,
):
    await conn.execute(
        """
        INSERT INTO
            contact_cards (
                owner_matrix_id,
                contact_name,
                contact_avatar_url,
                created_at,
                updated_at
            )
        VALUES
            (
                $1,
                $2,
                $3,
                DEFAULT,
                DEFAULT
            ) ON CONFLICT (owner_matrix_id) DO NOTHING;
        """,
        owner_matrix_id,
        contact_name,
        contact_avatar_url,
    )


async def get_contact_cards_by_owner(
    conn: asyncpg.Connection, owner_matrix_id: str
) -> list[ContactCard]:
    rows = await conn.fetch(
        """
        SELECT
            contact_name,
            contact_avatar_url
        FROM
            contact_cards
        WHERE
            owner_matrix_id = $1;
        """,
        owner_matrix_id,
    )
    return [ContactCard(**dict(row)) for row in rows]


async def update_contact_card(
    conn: asyncpg.Connection,
    owner_matrix_id: int,
    contact_name: str,
    contact_avatar_url: str | None = None,
):
    await conn.execute(
        """
        UPDATE contact_cards
        SET
            contact_name = $1,
            contact_avatar_url = $2,
            updated_at = CURRENT_TIMESTAMP
        WHERE
            owner_matrix_id = $3;
        """,
        contact_name,
        contact_avatar_url,
        owner_matrix_id,
    )


async def delete_contact_card(conn: asyncpg.Connection, owner_matrix_id: int):
    await conn.execute(
        """
        DELETE
        SELECT *
        FROM contact_cards WHERE
            owner_matrix_id = $1;
        """,
        owner_matrix_id,
    )
