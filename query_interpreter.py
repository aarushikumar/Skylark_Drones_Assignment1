from groq import Groq
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TOOLS = [
    "pipeline_by_sector",
    "top_deals",
    "work_order_status",
    "sector_pipeline_summary",
    "deals_by_stage",
    "sector_deal_count"
]


def interpret_query(question):

    prompt = f"""
You are a business intelligence assistant.

User question:
{question}

Available tools:

1. pipeline_by_sector (requires parameter: sector)
2. top_deals
3. work_order_status
4. sector_pipeline_summary
5. deals_by_stage
6. sector_deal_count

If the question mentions a sector like mining, telecom, powerline etc,
include it in params.

IMPORTANT:
Return ONLY valid JSON. Do NOT include explanations.

Examples:

{{"tool":"sector_pipeline_summary","params":{{}}}}

{{"tool":"deals_by_stage","params":{{}}}}

{{"tool":"sector_deal_count","params":{{}}}}

{{"tool":"work_order_status","params":{{}}}}

{{"tool":"pipeline_by_sector","params":{{"sector":"mining"}}}}

{{"tool":"top_deals","params":{{}}}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content

    match = re.search(r"\{.*\}", result, re.DOTALL)

    if match:
        try:
            parsed = json.loads(match.group())
        except:
            parsed = {"tool": "unknown", "params": {}}
    else:
        parsed = {"tool": "unknown", "params": {}}

    tool = parsed.get("tool", "unknown")
    params = parsed.get("params", {})

    # ensure tool is valid
    if tool not in TOOLS:
        tool = "unknown"

    return tool, params