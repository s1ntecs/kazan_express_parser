CREATE_SHOPS_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS shops(
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        shop_id TEXT NOT NULL,
        PRIMARY KEY (name, shop_id)
    );"""

CREATE_IMAGES_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS image(
        image_id SERIAL PRIMARY KEY,
        url TEXT NOT NULL,
        client_id INT NOT NULL,
        model_id INT,
        promt_id INT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES client(client_id),
        FOREIGN KEY (model_id) REFERENCES model(model_id),
        FOREIGN KEY (promt_id) REFERENCES promt(promt_id)
    );"""

CREATE_MODELS_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS model(
        model_id SERIAL PRIMARY KEY,
        model_name TEXT NOT NULL,
        model_token TEXT NOT NULL,
        client_id INT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES client(client_id)
    );"""

CREATE_PROMTS_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS promt(
        promt_id SERIAL PRIMARY KEY,
        promt_text TEXT NOT NULL,
        client_id INT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES client(client_id)
    );"""

CREATE_CATEGORIES_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS promt(
        promt_id SERIAL PRIMARY KEY,
        promt_text TEXT NOT NULL,
        client_id INT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES client(client_id)
    );"""

CREATE_GENRES_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS genre(
        my_genre_id SERIAL PRIMARY KEY,
        genre_id INT NOT NULL,
        client_id INT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES client(client_id)
    );"""

CREATE_GEN_WITH_MODEL_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS with_model(
        with_model_id SERIAL PRIMARY KEY,
        model_name TEXT NULL,
        client_id INT UNIQUE NOT NULL,
        FOREIGN KEY (client_id) REFERENCES client(client_id)
    );"""

CREATE_PROMT_EXAMPLE_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS promt_example(
        promt_id SERIAL PRIMARY KEY,
        promt_text TEXT NOT NULL
    );"""
