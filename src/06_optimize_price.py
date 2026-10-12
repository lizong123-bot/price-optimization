import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import os

df = pd.read_csv('../data/processed/enriched_data.csv')
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month

rf = joblib.load('../outputs/sales_model.pkl')
features = ['final_price', 'discount', 'competitor_price', 'inventory', 'month']

os.makedirs('../outputs/figures', exist_ok=True)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

results = []
sample_skus = ['SKU001', 'SKU010', 'SKU020', 'SKU030']

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.flatten()

for i, sku in enumerate(sample_skus):
    sub = df[df['sku'] == sku]
    if len(sub) == 0:
        continue
    avg_cost = sub['cost'].mean()
    avg_comp = sub['competitor_price'].mean()
    avg_inv = sub['inventory'].mean()
    avg_month = sub['month'].mean()
    current_price = sub['final_price'].mean()

    prices = np.linspace(avg_cost * 1.1, avg_cost * 3, 80)
    profits = []
    for p in prices:
        row = pd.DataFrame([[p, 0, avg_comp, avg_inv, avg_month]], columns=features)
        q = rf.predict(row)[0]
        profits.append((p - avg_cost) * q)
    profits = np.array(profits)

    best_idx = profits.argmax()
    best_price = prices[best_idx]
    best_profit = profits[best_idx]
    current_profit = (current_price - avg_cost) * rf.predict(
        pd.DataFrame([[current_price, 0, avg_comp, avg_inv, avg_month]], columns=features)
    )[0]

    results.append({
        'sku': sku,
        'cost': round(avg_cost, 2),
        'current_price': round(current_price, 2),
        'optimal_price': round(best_price, 2),
        'price_change_pct': round((best_price - current_price) / current_price * 100, 2),
        'current_profit': round(current_profit, 2),
        'optimal_profit': round(best_profit, 2),
        'profit_lift_pct': round((best_profit - current_profit) / current_profit * 100, 2)
    })

    axes[i].plot(prices, profits, color='#2ecc71')
    axes[i].axvline(best_price, color='r', linestyle='--',
                    label=f'最优价 {best_price:.0f}')
    axes[i].axvline(current_price, color='gray', linestyle=':',
                    label=f'当前价 {current_price:.0f}')
    axes[i].set_title(f'{sku} 价格-利润曲线')
    axes[i].set_xlabel('价格')
    axes[i].set_ylabel('预期利润')
    axes[i].legend(fontsize=8)

plt.tight_layout()
plt.savefig('../outputs/figures/price_profit_curve.png', dpi=120)

result_df = pd.DataFrame(results)
result_df.to_csv('../outputs/optimal_pricing.csv', index=False)
print("=" * 70)
print("利润最大化定价建议")
print("=" * 70)
print(result_df.to_string(index=False))
print("\n✅ 图表: ../outputs/figures/price_profit_curve.png")
print("✅ 结果: ../outputs/optimal_pricing.csv")