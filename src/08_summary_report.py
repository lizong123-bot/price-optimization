import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 读结果
cat_df = pd.read_csv('../outputs/elasticity_by_category.csv')
price_df = pd.read_csv('../outputs/optimal_pricing.csv')

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# ============ 图1：四象限策略图 ============
ax = axes[0]
x = cat_df['elasticity']
y = cat_df['avg_margin']
sizes = cat_df['avg_price'] * 8

colors = ['#e74c3c' if e < -1.5 else '#f39c12' if e < -0.8 else '#27ae60'
          for e in x]

ax.scatter(x, y, s=sizes, c=colors, alpha=0.7, edgecolors='black', linewidth=1.5)
for i, row in cat_df.iterrows():
    ax.annotate(row['category'], (row['elasticity'], row['avg_margin']),
                fontsize=12, ha='center', va='center', fontweight='bold')

ax.axvline(-1, color='gray', linestyle='--', alpha=0.5, label='弹性=-1 分界')
ax.axhline(y.mean(), color='gray', linestyle=':', alpha=0.5, label='平均毛利率')

# 象限标注
ax.text(-1.9, y.max()*0.98, '高敏感·高毛利\n→ 渗透定价', fontsize=10, color='#e74c3c')
ax.text(-0.5, y.max()*0.98, '低敏感·高毛利\n→ 溢价定价', fontsize=10, color='#27ae60')
ax.text(-1.9, y.min()*0.95, '高敏感·低毛利\n→ 清仓/促销', fontsize=10, color='#e74c3c')
ax.text(-0.5, y.min()*0.95, '低敏感·低毛利\n→ 优化成本', fontsize=10, color='#f39c12')

ax.set_xlabel('价格弹性', fontsize=12)
ax.set_ylabel('平均毛利率 (%)', fontsize=12)
ax.set_title('品类定价策略四象限图', fontsize=14, fontweight='bold')
ax.legend(loc='lower right')
ax.grid(alpha=0.3)

# ============ 图2：价格-利润对比 ============
ax = axes[1]
x_pos = np.arange(len(price_df))
width = 0.35

ax.bar(x_pos - width/2, price_df['current_profit'], width, label='当前利润', color='#95a5a6')
ax.bar(x_pos + width/2, price_df['optimal_profit'], width, label='最优利润', color='#2ecc71')

for i, row in price_df.iterrows():
    lift = row['profit_lift_pct']
    ax.annotate(f'+{lift:.1f}%',
                (i + width/2, row['optimal_profit']),
                ha='center', va='bottom', fontsize=10, fontweight='bold', color='#27ae60')

ax.set_xticks(x_pos)
ax.set_xticklabels(price_df['sku'])
ax.set_ylabel('利润')
ax.set_title('最优定价 vs 当前定价 - 利润提升', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('../outputs/figures/summary_dashboard.png', dpi=150, bbox_inches='tight')
print('✅ 总览图已保存: ../outputs/figures/summary_dashboard.png')