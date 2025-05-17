import requests
import psycopg2
import os
from datetime import datetime

# 為替API（例: ExchangeRate-API）
url = 'https://api.exchangerate.host/latest?base=USD&symbols=JPY'
response = requests.get(url)
data = response.json()
rate = data["rates"]["JPY"]

# DB接続
conn = psycopg2.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    dbname=os.environ["DB_NAME"],
    port=os.environ.get("DB_PORT", 5432)
)
cur = conn.cursor()

# テーブルがなければ作成
cur.execute("""
CREATE TABLE IF NOT EXISTS exchange_rates (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    usd_to_jpy NUMERIC
)
""")

# データ挿入
cur.execute("INSERT INTO exchange_rates (timestamp, usd_to_jpy) VALUES (%s, %s)",
            (datetime.utcnow(), rate))
conn.commit()

cur.close()
conn.close()
