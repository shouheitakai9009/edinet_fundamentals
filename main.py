import requests
import datetime
import pandas as pd

# 1日分のEDINETドキュメントを取得
documents_date = datetime.date(2022, 2, 15).strftime("%Y-%m-%d")
documents_request = requests.get(f"https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date={documents_date}&type=2")
documents = documents_request.json()['results']
df_documents = pd.DataFrame(documents)

# 有価証券報告書のみを取得
df_documents = df_documents.query('ordinanceCode == "010" and formCode == "020000" and xbrlFlag == "1"')

print(df_documents)