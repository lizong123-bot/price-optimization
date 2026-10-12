@echo off
cd /d "%~dp0src"

echo ===== 1. 生成数据 =====
python 01_generate_data.py
if errorlevel 1 goto error

echo ===== 2. 构建数据库 =====
python 02_load_to_sqlite.py
if errorlevel 1 goto error

echo ===== 3. SQL整合导出宽表 =====
python 03_run_sql.py
if errorlevel 1 goto error

echo ===== 4. 价格弹性分析 =====
python 04_elasticity.py
if errorlevel 1 goto error

echo ===== 5. 销量预测 =====
python 05_forecast.py
if errorlevel 1 goto error

echo ===== 6. 利润最大化 =====
python 06_optimize_price.py
if errorlevel 1 goto error

echo ===== 7. 策略输出 =====
python 07_strategy.py
if errorlevel 1 goto error

echo ===== 8. 总览报告 =====
python 08_summary_report.py
if errorlevel 1 goto error

echo.
echo ============================================
echo  全部完成！结果在 outputs/ 目录
echo ============================================
pause
exit /b 0

:error
echo.
echo ============================================
echo  执行出错，请检查上方红色输出
echo ============================================
pause
exit /b 1