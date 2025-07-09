import asyncpg


async def create_contact_cards_table(conn: asyncpg.Connection):
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS contact_cards (
            id SERIAL PRIMARY KEY,
            owner_matrix_id VARCHAR UNIQUE NOT NULL,
            contact_name VARCHAR NOT NULL,
            contact_avatar_url VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_owner_matrix_id ON contact_cards(owner_matrix_id);
    """)
    print("contact_cards table checked/created.")


async def create_platform_contacts_table(conn: asyncpg.Connection):
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS platform_contacts (
            id SERIAL PRIMARY KEY,
            contact_card_id INTEGER NOT NULL REFERENCES contact_cards (id) ON DELETE CASCADE,
            platform VARCHAR NOT NULL,
            platform_user_id VARCHAR NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (contact_card_id, platform)
        );
        CREATE INDEX IF NOT EXISTS idx_platform_user_id ON platform_contacts(platform_user_id);
    """)
    print("platform_contacts table checked/created.")


async def create_all_tables(conn: asyncpg.Connection):
    async with conn.transaction():
        await create_contact_cards_table(conn)
        await create_platform_contacts_table(conn)
