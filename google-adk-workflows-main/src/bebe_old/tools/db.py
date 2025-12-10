# src/bebe/tools/db.py
from google.cloud.sql.connector import Connector, IPTypes
import pg8000.native
import os
import psycopg2
import psycopg2.extras


# Connection name: project:region:instance
INSTANCE_CONNECTION_NAME = os.getenv("qwiklabs-gcp-00-eaa89c0a0427:us-central1:bebedb")  # e.g., "my-project:us-central1:my-postgres"
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "Passwordc412345!")
DB_NAME = os.getenv("DB_NAME", "bebedb")
IP_TYPE = IPTypes.PRIVATE if os.getenv("PRIVATE_IP") else IPTypes.PUBLIC


# Create a single connector; reuse across calls
connector = Connector(refresh_strategy="LAZY")  # reduces background refreshes; good for dev/serverless patterns



def get_conn():
    """
    Return a pg8000 DB-API connection via the Cloud SQL Python Connector.
    """
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
        ip_type=IP_TYPE,
    )
    return conn


def query_dicts(sql: str, params: tuple = ()):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            cols = [c[0] for c in cur.description] if cur.description else []
            rows = cur.fetchall()
            return [dict(zip(cols, r)) for r in rows]

def query_one(sql: str, params: tuple = ()):
    results = query_dicts(sql, params)
    return results[0] if results else None

    