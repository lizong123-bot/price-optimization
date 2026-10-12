import pandas as pd

cat_df = pd.read_csv('../outputs/elasticity_by_category.csv')

def suggest(row):
    if row['elasticity'] < -1.5:
        return '渗透定价：小幅降价(3-5%)换销量，主推爆款'
    elif row['elasticity'] < -0.8:
        return '稳健定价：跟随竞品价±3%，保利润'
    else:
        return '溢价定价：维持高价，主打品牌溢价'

def price_action(row):
    if row['elasticity'] < -1.5:
        return '降价3-5%'
    elif row['elasticity'] < -0.8:
        return '维持±3%'
    else:
        return '可提价5-8%'

cat_df['定价策略'] = cat_df.apply(suggest, axis=1)
cat_df['价格动作'] = cat_df.apply(price_action, axis=1)

cat_df.to_csv('../outputs/strategy.csv', index=False)

print("=" * 90)
print("分品类定价策略建议")
print("=" * 90)
for _, row in cat_df.iterrows():
    print(f"\n【{row['category']}】 弹性={row['elasticity']}, 均价={row['avg_price']}, 毛利率={row['avg_margin']}%")
    print(f"  → {row['定价策略']}")
    print(f"  → 建议动作：{row['价格动作']}")

# 生成报告
with open('../outputs/model_report.txt', 'w', encoding='utf-8') as f:
    f.write("电商价格策略与销量预测 - 分析报告\n")
    f.write("=" * 50 + "\n\n")
    f.write("一、价格弹性分析\n")
    f.write(cat_df.to_string(index=False))
    f.write("\n\n二、结论\n")
    f.write("1. 价格弹性整体在-1.5以下，说明用户对价格敏感\n")
    f.write("2. 女装弹性最高，适合渗透定价\n")
    f.write("3. 配饰弹性低，可维持高价保利润\n")
    f.write("4. 建议根据竞品价差动态调价，价差>10%时需响应\n")

print("\n✅ 策略文件: outputs/strategy.csv")
print("✅ 报告文件: outputs/model_report.txt")