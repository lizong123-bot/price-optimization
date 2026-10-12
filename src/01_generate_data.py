import pandas as pd
import numpy as np
import os

np.random.seed(42)
os.makedirs('../data/raw', exist_ok=True)

skus = [f'SKU{i:03d}' for i in range(1, 51)]
categories = ['女装', '鞋包', '配饰']
seasons = ['春', '夏', '秋', '冬']
dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')

# 1. 商品表
product = pd.DataFrame({
    'sku': skus,
    'category': np.random.choice(categories, len(skus)),
    'season': np.random.choice(seasons, len(skus)),
    'base_price': np.random.uniform(50, 500, len(skus)).round(2)
})

# 2. 成本表
cost = product[['sku']].copy()
cost['cost'] = (product['base_price'] * np.random.uniform(0.4, 0.6, len(skus))).round(2)

# 3. 销售流水
records = []
for sku in skus:
    base_p = product.loc[product.sku == sku, 'base_price'].values[0]
    for d in dates:
        price = round(base_p * np.random.uniform(0.85, 1.15), 2)
        discount = np.random.choice([0, 0, 0, 0.1, 0.2, 0.3],
                                    p=[0.5, 0.15, 0.15, 0.1, 0.06, 0.04])
        final_price = price * (1 - discount)
        elasticity = -1.8  # 真实弹性
        # ✅ 销量直接由绝对价格决定
        qty = max(0, int(
            200000 * (final_price ** elasticity) * np.random.uniform(0.7, 1.3)
        ))
        records.append([f'ORD{len(records):06d}', sku, d.strftime('%Y-%m-%d'),
                        qty, price, discount])

sales = pd.DataFrame(records, columns=['order_id', 'sku', 'date', 'qty', 'price', 'discount'])

# 4. 竞品价
comp = sales[['sku', 'date']].drop_duplicates().merge(product[['sku', 'base_price']], on='sku')
comp['competitor_price'] = (comp['base_price'] * np.random.uniform(0.9, 1.1, len(comp))).round(2)
comp = comp[['sku', 'date', 'competitor_price']]

# 5. 库存
inv = sales[['sku', 'date']].drop_duplicates().copy()
inv['inventory'] = np.random.randint(0, 1000, len(inv))

# 导出
sales.to_csv('../data/raw/sales.csv', index=False)
product.to_csv('../data/raw/product.csv', index=False)
cost.to_csv('../data/raw/cost.csv', index=False)
comp.to_csv('../data/raw/competitor_price.csv', index=False)
inv.to_csv('../data/raw/inventory.csv', index=False)

print(f'✅ 数据生成完成')
print(f'sales: {len(sales)} 行 | product: {len(product)} | cost: {len(cost)} | comp: {len(comp)} | inv: {len(inv)}')