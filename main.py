import requests
import psycopg2
import os
from datetime import datetime

# --- 為替レート取得 ---
url = "https://api.exchangerate.host/latest?base=USD&symbols=JPY"
response = requests.get(url)
data = response.json()
rate = data["rates"]["JPY"]
timestamp = datetime.utcnow()

# --- DB接続情報（Renderの環境変数から取得） ---
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT", "5432")
)

# --- データをテーブルに保存 ---
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS usd_jpy_rates (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL,
        rate NUMERIC NOT NULL
    );
""")
cur.execute("INSERT INTO usd_jpy_rates (timestamp, rate) VALUES (%s, %s);", (timestamp, rate))
conn.commit()
cur.close()
conn.close()

print(f"Inserted rate {rate} at {timestamp}")
