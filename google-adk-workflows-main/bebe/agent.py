"""
Root Bebe Agent
Talks to the customer to find the best products for them.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Import your tool functions
from bebe.tools.products import search_products, product_summary, suggest_upsell
from bebe.tools.pricing import price_with_discounts
from bebe.tools.cart import add_to_cart


SYSTEM_PROMPT = (
    "You are Bebe, a friendly shopping assistant. "
    "Ask brief clarifying questions (material, hobbies, price, brand, color, size, age). "
    "When recommending, ALWAYS return at most 10 products. "
    "Offer a 'Go to catalog' option anytime. "
    "Never force the user to start over. Keep details succinct. "
)

tools = [
    agent_tool(fn=search_products, name="search_products",
         description="Search products with filters and return up to 10."),
    agent_tool(fn=product_summary, name="product_summary",
         description="Get PDP summary for a product."),
    agent_tool(fn=price_with_discounts, name="price_with_discounts",
         description="Apply item and loyalty discounts; return final price and ETA."),
    agent_tool(fn=add_to_cart, name="add_to_cart",
         description="Add an item to the session cart with pricing."),
    agent_tool(fn=suggest_upsell, name="suggest_upsell",
         description="Suggest upsell items by brand.")
]

root_agent = LlmAgent(
    name="Bebe",
    instructions=SYSTEM_PROMPT,
    tools=tools,
    llm_config={
        "model": os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        # Provide API key via GOOGLE_API_KEY or use Vertex AI credentials
    },
    workflow="sequential"  # predictable pipeline for a demo
)

