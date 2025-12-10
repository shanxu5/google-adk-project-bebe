# src/bebe/tools/products.py
from .db import query_dicts, query_one

def search_products(query_text: str,
                    max_price: float | None = None,
                    brand: str | None = None):
    """
    Ranked FTS search over name+description+brand.
    Returns <= 10 products with basic fields for the carousel.
    """
    sql = """
    WITH q AS (SELECT to_tsquery('english', %s) AS tsq)
    SELECT id, name, image_url, price, brand, reviews_avg, reviews_count
    FROM products, q
    WHERE search_tsv @@ q.tsq
      AND (%s IS NULL OR price <= %s)
      AND (%s IS NULL OR brand ILIKE %s)
    ORDER BY ts_rank(search_tsv, q.tsq) DESC, reviews_avg DESC
    LIMIT 10;
    """
    # Convert free text to a conservative tsquery (split by spaces and AND them)
    tsquery = " & ".join([t for t in query_text.split() if t])
    params = (tsquery, max_price, max_price, brand, brand)
    return query_dicts(sql, params)

def product_summary(product_id: str):
    """
    PDP snippet: images, description, review summary, etc.
    """
    sql = """
    SELECT id, name, description, image_url, price, brand,
           reviews_avg, reviews_count, discount_amount
    FROM products
    WHERE id = %s
    """
    return query_one(sql, (product_id,))

def suggest_upsell(product_id: str):
    """
    Simple upsell: same brand (excluding the current item).
    """
    sql_brand = """
      SELECT brand, category FROM products WHERE id = %s
    """
    item = query_one(sql_brand, (product_id,))
    if not item:
        return []

    sql = """
    SELECT id, name, image_url, price, brand, reviews_avg, reviews_count
    FROM products
    WHERE id <> %s
      AND (brand = %s OR category = %s)
    ORDER BY reviews_avg DESC, price ASC
    LIMIT 4;
    """

def test_connection():
    return query_dicts("SELECT current_user, current_database();")
