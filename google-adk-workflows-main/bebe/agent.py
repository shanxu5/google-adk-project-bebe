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

# src/bebe/agents/bebe/agent.py
from adk import Agent

root_agent = Agent(
    name="Bebe",
    instructions=(
        "You are Bebe, a friendly shopping assistant. "
        "Ask brief clarifying questions (material, price, brand, color, size, age). "
        "Return at most 10 products when recommending. Offer a 'Go to catalog' option. "
        "Never force the user to start over. Keep details succinct."
    ),
    tools=[]  # We'll add search/pricing/cart tools in Step 2+
)
