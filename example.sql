-- create tables
CREATE TABLE contact_cards (
    id SERIAL PRIMARY KEY,
    owner_matrix_id VARCHAR UNIQUE NOT NULL,
    contact_name VARCHAR NOT NULL,
    contact_avatar_url VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE INDEX IF NOT EXISTS idx_user_id ON user_contacts(user_id);
-- CREATE INDEX IF NOT EXISTS idx_platform_user_id ON user_contacts(platform_user_id);
CREATE TABLE platform_contacts (
    id SERIAL PRIMARY KEY,
    contact_card_id INTEGER NOT NULL REFERENCES contact_card (id) ON DELETE CASCADE,
    platform VARCHAR NOT NULL,
    platform_user_id VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (contact_card_id, platform)
);

-- create contact card
INSERT INTO
    contact_card (
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
    ) ON CONFLICT (owner_matrix_id) DO NOTHING;

-- create platform contact
INSERT INTO
    platform_contact (
        contact_card_id,
        platform,
        platform_user_id,
        created_at,
        updated_at
    )
VALUES
    (
        1,
        'example_platform',
        'example_user_id',
        DEFAULT,
        DEFAULT
    ) ON CONFLICT (contact_card_id, platform) DO NOTHING;

-- update contact card
UPDATE contact_card
SET
    contact_name = 'Updated User',
    contact_avatar_url = 'https://example.com/updated_avatar.jpg',
    updated_at = CURRENT_TIMESTAMP
WHERE
    id = 1;

-- delete contact card
DELETE FROM contact_card
WHERE
    id = 1;

-- delete platform contact
DELETE FROM platform_contact
WHERE
    contact_card_id = 1
    AND platform = 'example_platform';

-- get all data owned by a user
SELECT
    contact_name,
    contact_avatar_url
FROM
    contact_card
WHERE
    owner_matrix_id = '@example:matrix.org';

SELECT
    card.id,
    platform.platform,
    platform.platform_user_id
FROM
    contact_card AS card
    INNER JOIN platform_contact AS platform ON card.id = platform.contact_card_id
WHERE
    card.owner_matrix_id = '@example:matrix.org';
