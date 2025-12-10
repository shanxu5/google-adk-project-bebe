# src/bebe/tools/cart.py
from collections import defaultdict
from .pricing import price_with_discounts

# super simple in-memory cart: {session_id: {product_id: qty}}
_CART = defaultdict(lambda: defaultdict(int))

def add_to_cart(session_id: str, product_id: str, qty: int = 1,
                user_id: str | None = None, coupon_code: str | None = None):
    _CART[session_id][product_id] += qty
    priced = price_with_discounts(user_id, product_id, coupon_code)
    return {
        "session_id": session_id,
        "line_item": {
            "product_id": product_id,
            "qty": _CART[session_id][product_id],
            "final_price": priced.get("final_price"),
            "eta_days": priced.get("eta_days"),
            "applied": priced.get("applied"),
        },
        "cart": dict(_CART[session_id])
    }
