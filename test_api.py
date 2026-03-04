from monday_api import get_board_items
from cleaning import clean_dataframe

WORK_ORDERS_BOARD_ID = 5026983950

df = get_board_items(WORK_ORDERS_BOARD_ID)

df = clean_dataframe(df)

print(df.dtypes)
print(df.head())
