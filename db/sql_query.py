CREATE_SHOPS_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS shops(
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        shop_id TEXT NOT NULL,
        PRIMARY KEY (name, shop_id)
    );"""
