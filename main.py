import requests
import datetime
import pandas as pd
from utils import file

# 1日分のEDINETドキュメントを取得
documents_date = datetime.date(2022, 2, 15).strftime("%Y-%m-%d")
documents_request = requests.get(f"https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date={documents_date}&type=2")
documents = documents_request.json()['results']
df_documents = pd.DataFrame(documents)

# 有価証券報告書のみを取得
df_documents = df_documents.query('ordinanceCode == "010" and formCode == "020000" and xbrlFlag == "1"')

# ZIPファイルをダウンロード
for i, documents_item in df_documents.iterrows():
  docID = documents_item['docID']
  response = requests.get(f"https://disclosure.edinet-fsa.go.jp/api/v1/documents/{docID}?type=1")
  file.zip_write(docID, response)
  file.select_file_in_zip(docID)
  file.move_xbrl(docID)
  file.remove_trash(docID)