from monday_api import get_board_items
from cleaning import clean_dataframe
from analytics import (
    pipeline_by_sector,
    top_deals,
    work_order_status,
    sector_pipeline_summary,
    deals_by_stage,
    sector_deal_count
)
from query_interpreter import interpret_query

import pandas as pd


DEALS_BOARD_ID = 5026983881
WORK_ORDERS_BOARD_ID = 5026983950


def answer_question(question):

    actions = []

    try:

        if not question or not question.strip():
            return "Please ask a valid business question.", []

        actions.append("Interpreting user question")

        try:
            tool, params = interpret_query(question)
        except Exception:
            actions.append("Query interpretation failed, using fallback")
            tool = "unknown"
            params = {}

        actions.append(f"Selected tool: {tool}")

        # ---------------------------------------------------
        # PIPELINE BY SECTOR
        # ---------------------------------------------------

        if tool == "pipeline_by_sector":

            actions.append("Fetching deals board")

            deals_df = clean_dataframe(get_board_items(DEALS_BOARD_ID))

            if deals_df is None or deals_df.empty:
                return "No deal data available.", actions

            sector = params.get("sector")

            if not sector:
                return "Please specify a sector (example: mining, telecom, energy).", actions

            actions.append(f"Calculating pipeline for sector: {sector}")

            value, count = pipeline_by_sector(deals_df, sector)

            if count == 0:
                return f"No deals found for sector '{sector}'.", actions

            response = f"""
Pipeline Summary

Sector: {sector.title()}
Number of Deals: {count}
Total Pipeline Value: ${value:,.0f}
"""

        # ---------------------------------------------------
        # TOP DEALS
        # ---------------------------------------------------

        elif tool == "top_deals":

            actions.append("Fetching deals board")

            deals_df = clean_dataframe(get_board_items(DEALS_BOARD_ID))

            if deals_df is None or deals_df.empty:
                return "No deal data available.", actions

            actions.append("Finding top deals")

            top = top_deals(deals_df)

            if top is None or top.empty:
                return "No deals available.", actions

            lines = ["Top Deals:\n"]

            for i, (_, row) in enumerate(top.iterrows(), 1):

                name = row.get("item", "Unknown Deal")
                value = row.get("masked deal value", 0)
                sector = row.get("sector/service", "Unknown")

                if pd.isna(name):
                    name = "Unknown Deal"

                if pd.isna(value):
                    value = 0

                if pd.isna(sector):
                    sector = "Unknown"

                lines.append(
                    f"{i}. {name.title()} — ${value:,.0f} — Sector: {sector.title()}"
                )

            response = "\n".join(lines)

        # ---------------------------------------------------
        # WORK ORDER STATUS
        # ---------------------------------------------------

        elif tool == "work_order_status":

            actions.append("Fetching work orders board")

            wo_df = clean_dataframe(get_board_items(WORK_ORDERS_BOARD_ID))

            if wo_df is None or wo_df.empty:
                return "No work order data available.", actions

            actions.append("Calculating work order status summary")

            status = work_order_status(wo_df)

            if not status:
                return "No work order status data available.", actions

            lines = ["Work Order Status:\n"]

            for s, c in status.items():
                lines.append(f"{s.title()}: {c}")

            response = "\n".join(lines)

        # ---------------------------------------------------
        # SECTOR PIPELINE SUMMARY
        # ---------------------------------------------------

        elif tool == "sector_pipeline_summary":

            actions.append("Fetching deals board")

            deals_df = clean_dataframe(get_board_items(DEALS_BOARD_ID))

            summary = sector_pipeline_summary(deals_df)

            if summary is None or summary.empty:
                return "No sector pipeline data available.", actions

            lines = ["Pipeline by Sector:\n"]

            for sector, value in summary.items():
                lines.append(f"{sector.title()} — ${value:,.0f}")

            response = "\n".join(lines)

        # ---------------------------------------------------
        # DEALS BY STAGE
        # ---------------------------------------------------

        elif tool == "deals_by_stage":

            actions.append("Fetching deals board")

            deals_df = clean_dataframe(get_board_items(DEALS_BOARD_ID))

            stage_counts = deals_by_stage(deals_df)

            if stage_counts is None or stage_counts.empty:
                return "No deal stage data available.", actions

            lines = ["Deals by Stage:\n"]

            for stage, count in stage_counts.items():
                lines.append(f"{stage.title()} — {count} deals")

            response = "\n".join(lines)

        # ---------------------------------------------------
        # DEAL COUNT BY SECTOR
        # ---------------------------------------------------

        elif tool == "sector_deal_count":

            actions.append("Fetching deals board")

            deals_df = clean_dataframe(get_board_items(DEALS_BOARD_ID))

            sector_counts = sector_deal_count(deals_df)

            if sector_counts is None or sector_counts.empty:
                return "No sector deal data available.", actions

            lines = ["Deals by Sector:\n"]

            for sector, count in sector_counts.items():
                lines.append(f"{sector.title()} — {count} deals")

            response = "\n".join(lines)

        # ---------------------------------------------------
        # UNKNOWN TOOL
        # ---------------------------------------------------

        else:

            response = """
I couldn't understand the question.

You can ask things like:

• Show top deals
• What is the pipeline in mining sector?
• How many work orders are completed?
• Which sector has the biggest pipeline?
• How many deals are in each stage?
"""

        return response.strip(), actions

    except Exception as e:

        return f"An unexpected error occurred: {str(e)}", actions