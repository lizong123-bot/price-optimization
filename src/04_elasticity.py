import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('../outputs/figures', exist_ok=True)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('../data/processed/enriched_data.csv')
df['log_price'] = np.log(df['final_price'])
df['log_sales'] = np.log(df['sales'] + 1)
df['season_dummy'] = (df['season'] == '夏').astype(int)

# 整体回归
X = sm.add_constant(df[['log_price', 'discount', 'competitor_price', 'season_dummy']])
model = sm.OLS(df['log_sales'], X).fit()
print("=" * 50)
print("整体价格弹性回归")
print("=" * 50)
print(model.summary())
print(f"\n📊 价格弹性 = {model.params['log_price']:.3f}")
print(f"   解读：价格每上涨1%，销量变化 {model.params['log_price']:.2f}%")

# 分品类
cat_results = []
for cat in df['category'].unique():
    sub = df[df['category'] == cat].copy()
    sub['log_p'] = np.log(sub['final_price'])
    sub['log_q'] = np.log(sub['sales'] + 1)
    Xc = sm.add_constant(sub[['log_p', 'discount', 'competitor_price']])
    m = sm.OLS(sub['log_q'], Xc).fit()
    cat_results.append({
        'category': cat,
        'elasticity': round(m.params['log_p'], 3),
        'r2': round(m.rsquared, 3),
        'p_value': round(m.pvalues['log_p'], 4),
        'avg_price': round(sub['final_price'].mean(), 1),
        'avg_margin': round(((sub['final_price'] - sub['cost']) / sub['final_price']).mean() * 100, 1)
    })

cat_df = pd.DataFrame(cat_results).sort_values('elasticity')
print("\n" + "=" * 50)
print("分品类价格弹性")
print("=" * 50)
print(cat_df.to_string(index=False))
cat_df.to_csv('../outputs/elasticity_by_category.csv', index=False)

# 可视化
fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#e74c3c' if e < -1.5 else '#f39c12' if e < -0.8 else '#27ae60'
          for e in cat_df['elasticity']]
ax.barh(cat_df['category'], cat_df['elasticity'], color=colors)
ax.axvline(-1, color='gray', linestyle='--', label='弹性=-1 分界')
ax.set_xlabel('价格弹性')
ax.set_title('各品类价格弹性')
ax.legend()
plt.tight_layout()
plt.savefig('../outputs/figures/elasticity_by_category.png', dpi=120)
print("\n✅ 图表已保存: ../outputs/figures/elasticity_by_category.png")