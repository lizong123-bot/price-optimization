import sqlite3
import pandas as pd
import math

conn = sqlite3.connect('../data/price.db')

# ✅ 注册 sqrt 函数给 SQLite 用
conn.create_function("SQRT", 1, math.sqrt)

with open('../sql/02_etl.sql', 'r', encoding='utf-8') as f:
    etl_sql = f.read()

df = pd.read_sql_query(etl_sql, conn)
df.to_csv('../data/processed/enriched_data.csv', index=False)
print(f'✅ 宽表导出: {len(df)} 行 × {len(df.columns)} 列')
print('列名:', list(df.columns))

# 异常值检测
with open('../sql/03_anomaly.sql', 'r', encoding='utf-8') as f:
    anomaly_sql = f.read()
anomaly = pd.read_sql_query(anomaly_sql, conn)
print(f'⚠️  检测到 {len(anomaly)} 条价格异常记录')

conn.close()