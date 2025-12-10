# src/bebe/tools/products.py
from .db import query_dicts, query_one

def search_products(query_text: str,
                    max_price: float | None = None,
                    brand: str | None = None):
    """
    Loosened search with fallbacks:
    1) Apply price/brand + text filters.
    2) If none, drop price/brand, keep text.
    3) If none, return top 10 by price (no filters).
    """
    q = query_text.strip() if query_text is not None else None
    q_filter = q or None  # None skips text filter

    sql = """
    SELECT id, product_name, image_url, price, brand
    FROM product
    WHERE (%s IS NULL OR price::numeric <= %s::numeric)
      AND (%s IS NULL OR brand ILIKE %s)
      AND (%s IS NULL
           OR product_name ILIKE %s
           OR description ILIKE %s
           OR brand ILIKE %s)
    ORDER BY price ASC
    LIMIT 10;
    """
    params = (
        max_price, max_price,
        brand, f"%{brand}%" if brand else None,
        q_filter,
        f"%{q_filter}%", f"%{q_filter}%", f"%{q_filter}%"
    )
    rows = query_dicts(sql, params)
    if rows:
        return rows

    # Fallback: drop price/brand, keep text if provided
    fallback_sql = """
    SELECT id, product_name, image_url, price, brand
    FROM product
    WHERE (%s IS NULL
           OR product_name ILIKE %s
           OR description ILIKE %s
           OR brand ILIKE %s)
    ORDER BY price ASC
    LIMIT 10;
    """
    fallback_params = (
        q_filter,
        f"%{q_filter}%", f"%{q_filter}%", f"%{q_filter}%"
    )
    rows = query_dicts(fallback_sql, fallback_params)
    if rows:
        return rows

    # Final fallback: top 10 by price, no filters
    return query_dicts(
        """
        SELECT id, product_name, image_url, price, brand
        FROM product
        ORDER BY price ASC
        LIMIT 10;
        """,
        ()
    )

def product_summary(product_id: str):
    """
    PDP snippet: images, description, review summary, etc.
    """
    sql = """
    SELECT id, product_name, description, image_url, price, brand, discount_amount
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
