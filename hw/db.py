"""The module for connecting to the database."""
import os

import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

dotenv.load_dotenv()


def connect() -> psycopg2.extensions.connection:
    """Connect to the database.

    Returns:
        an object of the connection class.
    """
    creds = {
        'port': os.getenv('POSTGRES_PORT'),
        'host': os.getenv('POSTGRES_HOST'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'database': os.getenv('POSTGRES_DB'),
    }
    return psycopg2.connect(**creds, cursor_factory=RealDictCursor)
