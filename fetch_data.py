import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = "1IY9MJAq1WQEMR98I2cle4VcKB6i0Dd5E-8Nx1wE-iX4"
RANGE = "A:E"

credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)

service = build("sheets", "v4", credentials=credentials)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
rows = result.get("values", [])

data = []
for row in rows[1:]:
    if len(row) >= 1 and row[0].strip():
        data.append({
            "cod":    row[0].strip() if len(row) > 0 else "",
            "end":    row[1].strip() if len(row) > 1 else "",
            "bairro": row[2].strip() if len(row) > 2 else "",
            "cidade": row[3].strip() if len(row) > 3 else "",
            "data":   row[4].strip() if len(row) > 4 else ""
        })

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

print(f"{len(data)} imóveis exportados para data.json")
