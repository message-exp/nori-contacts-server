-- create tables
CREATE TABLE IF NOT EXISTS contact_cards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_matrix_id VARCHAR NOT NULL,
    contact_name VARCHAR NOT NULL,
    nickname VARCHAR,
    contact_avatar_url VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE INDEX IF NOT EXISTS idx_user_id ON user_contacts(user_id);
-- CREATE INDEX IF NOT EXISTS idx_platform_user_id ON user_contacts(platform_user_id);
CREATE TABLE IF NOT EXISTS platform_contacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contact_card_id UUID NOT NULL REFERENCES contact_cards (id) ON DELETE CASCADE,
    platform VARCHAR NOT NULL,
    platform_user_id VARCHAR NOT NULL,
    dm_room_id VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (contact_card_id, platform, platform_user_id)
);  

-- create contact card
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
        '@example:matrix.org',
        'Example User',
        'https://example.com/avatar.jpg',
        DEFAULT,
        DEFAULT
    );

-- create platform contact
INSERT INTO
    platform_contacts (
        contact_card_id,
        platform,
        platform_user_id,
        dm_room_id,
        created_at,
        updated_at
    )
VALUES
    (
        1,
        'example_platform',
        'example_user_id',
        '123',
        DEFAULT,
        DEFAULT
    ) ON CONFLICT (contact_card_id, platform, platform_user_id) DO NOTHING;

-- update contact card
UPDATE contact_cards
SET
    contact_name = 'Updated User',
    contact_avatar_url = 'https://example.com/updated_avatar.jpg',
    updated_at = CURRENT_TIMESTAMP
WHERE
    id = 1;

-- delete contact card
DELETE FROM contact_cards
WHERE
    id = 1;

-- delete platform contact
DELETE FROM platform_contacts
WHERE
    contact_card_id = 1
    AND platform = 'example_platform';

-- get all data owned by a user
SELECT
    contact_name,
    contact_avatar_url
FROM
    contact_cards
WHERE
    owner_matrix_id = '@example:matrix.org';

SELECT
    card.id,
    platform.platform,
    platform.platform_user_id
FROM
    contact_cards AS card
    INNER JOIN platform_contacts AS platform ON card.id = platform.contact_card_id
WHERE
    card.owner_matrix_id = '@example:matrix.org';
