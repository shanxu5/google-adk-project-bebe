# src/bebe/tools/pricing.py
from .db import query_one

def price_with_discounts(user_id: str | None, product_id: str, coupon_code: str | None = None):
    item = query_one("""
        SELECT id, price, discount_amount FROM products WHERE id = %s
    """, (product_id,))
    if not item:
        return {"error": "product_not_found"}

    user = query_one("""
        SELECT id, is_pro, loyalty_tier FROM users WHERE id = %s
    """, (user_id,)) if user_id else None

    price = max(0.0, float(item["price"]) - float(item.get("discount_amount") or 0.0))
    # Loyalty multiplier (mock)
    if user and user.get("is_pro"):
        price *= 0.95
    # Simple coupon (mock)
    if coupon_code == "WELCOME10":
        price *= 0.90

    # Demo ETA (mock logic)
    eta_days = 5 if user and user.get("is_pro") else 7
    return {
        "product_id": product_id,
        "base_price": float(item["price"]),
        "final_price": round(price, 2),
        "applied": {
            "item_discount": float(item.get("discount_amount") or 0.0),
            "loyalty": bool(user and user.get("is_pro")),
            "coupon": coupon_code or None
        },
        "eta_days": eta_days
    }
