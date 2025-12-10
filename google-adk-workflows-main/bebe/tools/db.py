# src/bebe/tools/db.py
import os
import psycopg2
import psycopg2.extras

# Direct connection string (preferred for local/dev)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Please set it in your .env (e.g., postgresql://user:pass@host:5432/dbname).")



def get_conn():
    """Return a psycopg2 connection using DATABASE_URL."""
    return psycopg2.connect(DATABASE_URL)


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

    