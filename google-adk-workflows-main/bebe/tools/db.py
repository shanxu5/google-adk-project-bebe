# src/bebe/tools/db.py
from google.cloud.sql.connector import Connector
import pg8000.native
import os
import psycopg2
import psycopg2.extras


# Connection name: project:region:instance
INSTANCE_CONNECTION_NAME = os.getenv("qwiklabs-gcp-00-eaa89c0a0427:us-central1:bebedb")  # e.g., "my-project:us-central1:my-postgres"
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "Passwordc412345!")
DB_NAME = os.getenv("DB_NAME", "bebedb")

connector = Connector()

def get_conn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn


def query_dicts(sql: str, params: dict | tuple = ()):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall()

def query_one(sql: str, params: dict | tuple = ()):
    rows = query_dicts(sql, params)
    