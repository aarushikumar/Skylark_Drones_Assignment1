def pipeline_by_sector(df, sector):
    sector = sector.lower()
    filtered = df[df["sector/service"] == sector]
    total_value = filtered["masked deal value"].sum()
    deal_count = len(filtered)
    return total_value, deal_count

def top_deals(df, n=5):
    df = df.sort_values("masked deal value", ascending=False)
    return df.head(n)

def deals_by_sector(df):
    return df.groupby("sector/service").size().sort_values(ascending=False)

def work_order_status(df):
    return df["execution status"].value_counts()

import pandas as pd


def sector_pipeline_summary(df):
    """Total pipeline value grouped by sector"""

    if "sector/service" not in df.columns or "masked deal value" not in df.columns:
        return None

    summary = (
        df.groupby("sector/service")["masked deal value"]
        .sum()
        .sort_values(ascending=False)
    )

    return summary


def deals_by_stage(df):
    """Count deals in each pipeline stage"""

    if "deal stage" not in df.columns:
        return None

    return df["deal stage"].value_counts()


def sector_deal_count(df):
    """Number of deals per sector"""

    if "sector/service" not in df.columns:
        return None

    return df["sector/service"].value_counts()