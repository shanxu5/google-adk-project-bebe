# src/bebe/tools/db.py
import os
import psycopg2
import psycopg2.extras

DATABASE_URL = os.getenv("DATABASE_URL")  # e.g., postgresql://user:pass@host/db

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def query_dicts(sql: str, params: dict | tuple = ()):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall()

def query_one(sql: str, params: dict | tuple = ()):
    rows = query_dicts(sql, params)
