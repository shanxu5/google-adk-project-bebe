# src/bebe/tools/products.py
from .db import query_dicts, query_one

def search_products(query_text: str,
                    max_price: float | None = None,
                    brand: str | None = None):
    sql = """
    WITH q AS (SELECT to_tsquery('english', %s) AS tsq)
    SELECT id, product_name, image_url, price, brand
    FROM product
    WHERE (%s IS NULL OR price <= %s)
      AND (%s IS NULL OR brand ILIKE %s)
      AND (product_name ILIKE %s OR description ILIKE %s OR brand ILIKE %s)
    ORDER BY price ASC
    LIMIT 10;
    """
    params = (
        query_text,          # for to_tsquery
        max_price, max_price,
        brand, f"%{brand}%" if brand else None,
        f"%{query_text}%", f"%{query_text}%", f"%{query_text}%"
    )
    return query_dicts(sql, params)

def product_summary(product_id: str):
    """
    PDP snippet: images, description, review summary, etc.
    """
    sql = """
    SELECT id, name, description, image_url, price, brand,discount_amount
    FROM product
    WHERE id = %s
    """
    return query_one(sql, (product_id,))

def suggest_upsell(product_id: str):
    """
    Simple upsell: same brand (excluding the current item).
    """
    sql_brand = """
      SELECT brand, category FROM product WHERE id = %s
    """
    item = query_one(sql_brand, (product_id,))
    if not item:
        return []

    sql = """
    SELECT id, name, image_url, price, brand, reviews_avg, reviews_count
    FROM product
    WHERE id <> %s
      AND (brand = %s OR category = %s)
    ORDER BY reviews_avg DESC, price ASC
    LIMIT 4;
    """

def test_connection():
    return query_dicts("SELECT current_user, current_database();")
