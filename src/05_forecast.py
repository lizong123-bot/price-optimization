import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error, r2_score
import matplotlib.pyplot as plt
import os

import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('../data/processed/enriched_data.csv')
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month

features = ['final_price', 'discount', 'competitor_price', 'inventory', 'month']
df_model = df.dropna(subset=features + ['sales'])

X_tr, X_te, y_tr, y_te = train_test_split(
    df_model[features], df_model['sales'], test_size=0.2, random_state=42
)

rf = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)
rf.fit(X_tr, y_tr)
pred = rf.predict(X_te)

print("=" * 50)
print("销量预测模型")
print("=" * 50)
print(f"R²  = {r2_score(y_te, pred):.3f}")
print(f"MAPE = {mean_absolute_percentage_error(y_te, pred):.2%}")

# 特征重要性
imp = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)
print("\n特征重要性：")
print(imp.to_string())

fig, ax = plt.subplots(figsize=(7, 4))
imp.plot(kind='barh', ax=ax, color='#3498db')
ax.set_xlabel('重要性')
ax.set_title('销量预测特征重要性')
plt.tight_layout()
plt.savefig('../outputs/figures/feature_importance.png', dpi=120)

# 保存模型
import joblib
os.makedirs('../outputs', exist_ok=True)
joblib.dump(rf, '../outputs/sales_model.pkl')
print("\n✅ 模型已保存: outputs/sales_model.pkl")