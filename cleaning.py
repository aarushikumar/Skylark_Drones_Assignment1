import pandas as pd



import pandas as pd


def clean_dataframe(df):

    if df is None:
        return pd.DataFrame()

    df = df.copy()

    # ---------------------------------------------------
    # NORMALIZE COLUMN NAMES
    # ---------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    # ---------------------------------------------------
    # CLEAN TEXT VALUES
    # ---------------------------------------------------

    for col in df.columns:

        if df[col].dtype == "object":

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .replace({"": pd.NA, "nan": pd.NA})
            )

            # convert to lowercase for consistency
            df[col] = df[col].str.lower()

    # ---------------------------------------------------
    # CLEAN NUMERIC DEAL VALUES
    # ---------------------------------------------------

    if "masked deal value" in df.columns:

        df["masked deal value"] = (
            df["masked deal value"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
        )

        df["masked deal value"] = pd.to_numeric(
            df["masked deal value"],
            errors="coerce"
        )

    # ---------------------------------------------------
    # DATE CLEANING
    # ---------------------------------------------------

    date_columns = [
        "tentative close date",
        "close date (a)",
        "created date",
        "data delivery date",
        "probable start date",
        "probable end date",
        "collection date"
    ]

    for col in date_columns:

        if col in df.columns:

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce",
                infer_datetime_format=True
            )

    # ---------------------------------------------------
    # DROP FULLY EMPTY ROWS
    # ---------------------------------------------------

    df.dropna(how="all", inplace=True)

    return df