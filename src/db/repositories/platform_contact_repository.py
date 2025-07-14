from uuid import UUID
import asyncpg

from models import PlatformContact


async def insert_platform_contact(
    conn: asyncpg.Connection,
    contact_card_id: UUID,
    platform: str,
    platform_user_id: str,
):
    row = await conn.fetchrow(
        """
        INSERT INTO platform_contacts (
            contact_card_id,
            platform,
            platform_user_id,
            created_at,
            updated_at
        )
        VALUES(
            $1,
            $2,
            $3,
            DEFAULT,
            DEFAULT
        )
        ON CONFLICT (contact_card_id, platform) DO NOTHING
        RETURNING contact_card_id, platform, platform_user_id;
        """,
        contact_card_id,
        platform,
        platform_user_id,
    )
    return PlatformContact(**row) if row else None


async def get_platform_contacts_by_owner(
    conn: asyncpg.Connection, owner_matrix_id: str
) -> list[PlatformContact]:
    rows = await conn.fetch(
        """
        SELECT
            card.id AS contact_card_id,
            platform.platform,
            platform.platform_user_id
        FROM
            contact_cards AS card
            INNER JOIN platform_contacts AS platform ON card.id = platform.contact_card_id
        WHERE
            card.owner_matrix_id = $1;
        """,
        owner_matrix_id,
    )
    return [PlatformContact(**row) for row in rows]


async def get_platform_contacts_by_contact_card_id(
    conn: asyncpg.Connection, contact_card_id: UUID
) -> list[PlatformContact]:
    rows = await conn.fetch(
        """
        SELECT
            contact_card_id,
            platform,
            platform_user_id
        FROM
            platform_contacts
        WHERE
            contact_card_id = $1;
        """,
        contact_card_id,
    )
    return [PlatformContact(**row) for row in rows]


async def get_platform_contacts_by_contact_card_id_and_platform(
    conn: asyncpg.Connection, contact_card_id: UUID, platform: str
) -> list[PlatformContact]:
    row = await conn.fetchrow(
        """
        SELECT
            contact_card_id,
            platform,
            platform_user_id
        FROM
            platform_contacts
        WHERE
            contact_card_id = $1
            AND platform = $2;
        """,
        contact_card_id,
        platform,
    )
    return PlatformContact(**row) if row else None


async def update_platform_contact_user_id(
    conn: asyncpg.Connection,
    contact_card_id: UUID,
    platform: str,
    platform_user_id: str,
):
    row = await conn.fetchrow(
        """
        UPDATE platform_contacts
        SET
            platform_user_id = $1,
            updated_at = CURRENT_TIMESTAMP
        WHERE
            contact_card_id = $2
            AND platform = $3
        RETURNING contact_card_id, platform, platform_user_id;
        """,
        platform_user_id,
        contact_card_id,
        platform,
    )
    return PlatformContact(**row) if row else None


async def delete_platform_contact(
    conn: asyncpg.Connection, contact_card_id: UUID, platform: str
):
    await conn.execute(
        """
        DELETE 
        -- SELECT *
        FROM platform_contacts WHERE
            contact_card_id = $1
            AND platform = $2;
        """,
        contact_card_id,
        platform,
    )
