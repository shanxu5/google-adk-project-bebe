"""
Root Bebe Agent
Talks to the customer to find the best products for them.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import function_tool
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# src/bebe/agents/bebe/agent.py
#from google.adk import Agent, Tool


# Import your tool functions
from bebe.tools.products import search_products, product_summary, suggest_upsell
from bebe.tools.pricing import price_with_discounts
from bebe.tools.cart import add_to_cart


SYSTEM_PROMPT = (
    "You are Bebe, a friendly shopping assistant. Always introduce yourself at the beginning of the conversation."
    "Ask brief clarifying questions (price, brand, color). "
    "Alway show the image url for each product."
    "For each product, show the original price crossed out and the discounted price in bold next to it."
    "When recommending, ALWAYS return at most 10 products. "
    "Offer a 'Go to catalog' option anytime. "
    "Never force the user to start over. Keep details succinct. "
)

tools = [
    function_tool.FunctionTool(search_products),
    function_tool.FunctionTool(product_summary),
    function_tool.FunctionTool(price_with_discounts),
    function_tool.FunctionTool(add_to_cart),
    function_tool.FunctionTool(suggest_upsell),
]

root_agent = LlmAgent(
    name="Bebe",
    instruction=SYSTEM_PROMPT,
    model=os.getenv("MODEL_NAME", "gemini-2.5-flash"),
    tools=tools,
)

