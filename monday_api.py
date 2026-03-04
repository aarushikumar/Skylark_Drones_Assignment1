import requests
import pandas as pd

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYyODU4MTY0MywiYWFpIjoxMSwidWlkIjoxMDA1NzIwODIsImlhZCI6IjIwMjYtMDMtMDRUMDU6MzM6MzQuMDAwWiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjM0MDY0MTA2LCJyZ24iOiJhcHNlMiJ9.QxheaC5FwZGxOVgSL__uG0X_SwumzA-FtblcxU8Ms_k"
URL = "https://api.monday.com/v2"

headers = {
    "Authorization": API_KEY
}


def get_board_items(board_id):

    query = f"""
    {{
      boards(ids: {board_id}) {{
        items_page {{
          items {{
            name
            column_values {{
              text
              column {{
                title
              }}
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(URL, json={'query': query}, headers=headers)

    data = response.json()

    items = data["data"]["boards"][0]["items_page"]["items"]

    rows = []

    for item in items:

        row = {"Item": item["name"]}

        for col in item["column_values"]:
            row[col["column"]["title"]] = col["text"]

        rows.append(row)

    df = pd.DataFrame(rows)

    return df