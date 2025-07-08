import asyncpg

from models import PlatformContact


async def insert_platform_contact(
    conn: asyncpg.Connection, owner_matrix_id: str, platform: str, platform_user_id: str
):
    await conn.execute(
        """
        INSERT INTO platform_contacts (
            contact_card_id,
            platform,
            platform_user_id,
            created_at,
            updated_at
        )
        SELECT
            id,
            $1,
            $2,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        FROM 
            contact_cards
        WHERE 
            owner_matrix_id = $3
        ON CONFLICT (contact_card_id, platform) DO NOTHING;
    """,
        platform,
        platform_user_id,
        owner_matrix_id,
    )


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
    return [PlatformContact(**dict(row)) for row in rows]


async def update_platform_contact_user_id(
    conn: asyncpg.Connection,
    owner_matrix_id: str,
    platform: str,
    platform_user_id: str,
):
    await conn.execute(
        """
        UPDATE platform_contacts
        SET
            platform_user_id = $1,
            updated_at = CURRENT_TIMESTAMP
        WHERE
            contact_card_id = (
                SELECT id FROM contact_cards WHERE owner_matrix_id = $2
            )
            AND platform = $3;
        """,
        platform_user_id,
        owner_matrix_id,
        platform,
    )


async def delete_platform_contact(
    conn: asyncpg.Connection, contact_card_id: int, platform: str
):
    await conn.execute(
        """
        DELETE FROM platform_contacts
        WHERE
            contact_card_id = $1
            AND platform = $2;
    """,
        contact_card_id,
        platform,
    )
