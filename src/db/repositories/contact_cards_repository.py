from uuid import UUID
import asyncpg

from models import ContactCard


async def insert_contact_card(
    conn: asyncpg.Connection,
    owner_matrix_id: str,
    contact_name: str,
    nickname: str | None = None,
    contact_avatar_url: str | None = None,
) -> ContactCard:
    row = await conn.fetchrow(
        """
        INSERT INTO
            contact_cards (
                owner_matrix_id,
                contact_name,
                nickname,
                contact_avatar_url,
                created_at,
                updated_at
            )
        VALUES
            (
                $1,
                $2,
                $3,
                $4,
                DEFAULT,
                DEFAULT
            )
        RETURNING id, contact_name, nickname, contact_avatar_url
        """,
        owner_matrix_id,
        contact_name,
        nickname,
        contact_avatar_url,
    )
    return ContactCard(**row)


async def get_contact_cards_by_owner(
    conn: asyncpg.Connection, owner_matrix_id: str
) -> list[ContactCard]:
    rows = await conn.fetch(
        """
        SELECT
            id,
            contact_name,
            nickname,
            contact_avatar_url
        FROM
            contact_cards
        WHERE
            owner_matrix_id = $1;
        """,
        owner_matrix_id,
    )
    return [ContactCard(**row) for row in rows]


async def get_single_contact_card_by_id_and_owner(
    conn: asyncpg.Connection, id: UUID, owner_matrix_id: str
) -> ContactCard | None:
    row = await conn.fetchrow(
        """
        SELECT
            id,
            contact_name,
            nickname,
            contact_avatar_url
        FROM
            contact_cards
        WHERE
            id = $1
            AND owner_matrix_id = $2;
        """,
        id,
        owner_matrix_id,
    )
    return ContactCard(**row) if row else None


async def update_contact_card(
    conn: asyncpg.Connection,
    id: UUID,
    contact_name: str,
    nickname: str | None = None,
    contact_avatar_url: str | None = None,
) -> ContactCard | None:
    row = await conn.fetchrow(
        """
        UPDATE contact_cards
        SET
            contact_name = $1,
            nickname = $2,
            contact_avatar_url = $3,
            updated_at = CURRENT_TIMESTAMP
        WHERE
            id = $4
        RETURNING id, contact_name, nickname, contact_avatar_url;
        """,
        contact_name,
        nickname,
        contact_avatar_url,
        id,
    )
    return ContactCard(**row) if row else None


async def delete_contact_card(conn: asyncpg.Connection, id: UUID):
    await conn.execute(
        """
        DELETE
        -- SELECT *
        FROM contact_cards WHERE
            id = $1;
        """,
        id,
    )
