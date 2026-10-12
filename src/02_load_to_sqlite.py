import sqlite3
import pandas as pd
import os

os.makedirs('../data/processed', exist_ok=True)

# ✅ 每次运行前删除旧数据库，避免数据重复
if os.path.exists('../data/price.db'):
    os.remove('../data/price.db')
    print('🗑️  已删除旧数据库')

conn = sqlite3.connect('../data/price.db')

# 建表
with open('../sql/01_schema.sql', 'r', encoding='utf-8') as f:
    conn.executescript(f.read())

# 导入CSV
tables = ['sales', 'product', 'cost', 'competitor_price', 'inventory']
for t in tables:
    df = pd.read_csv(f'../data/raw/{t}.csv')
    df.to_sql(t, conn, if_exists='append', index=False)
    print(f'✅ {t}: {len(df)} 行导入')

conn.commit()
conn.close()
print('✅ 数据库构建完成: data/price.db')