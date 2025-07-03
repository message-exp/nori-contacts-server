import asyncpg


async def create_user_contacts_table(conn: asyncpg.Connection):
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS user_contacts (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            platform_user_id TEXT NOT NULL,
            platform_username TEXT NOT NULL,
            platform TEXT NOT NULL,
            avatar TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (platform, platform_user_id)
        )
        CREATE INDEX IF NOT EXISTS idx_user_id ON user_contacts(user_id);
        CREATE INDEX IF NOT EXISTS idx_platform_user_id ON user_contacts(platform_user_id);
    """)
    print("user_contacts table checked/created.")


async def create_tables(conn: asyncpg.Connection):
    async with conn.transaction():
        await create_user_contacts_table(conn)
