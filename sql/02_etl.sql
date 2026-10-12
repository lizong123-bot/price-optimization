WITH base AS (
    SELECT
        s.order_id,
        s.sku,
        s.date,
        s.qty,
        s.price,
        s.discount,
        ROUND(s.price * (1 - s.discount), 2) AS final_price,
        p.category,
        p.season,
        p.base_price,
        c.cost,
        cp.competitor_price,
        i.inventory,
        ROUND(s.price * (1 - s.discount) - c.cost, 2) AS unit_profit
    FROM sales s
    LEFT JOIN product p ON s.sku = p.sku
    LEFT JOIN cost c ON s.sku = c.sku
    LEFT JOIN competitor_price cp ON s.sku = cp.sku AND s.date = cp.date
    LEFT JOIN inventory i ON s.sku = i.sku AND s.date = i.date
),
enriched AS (
    SELECT *,
        LAG(final_price) OVER (PARTITION BY sku ORDER BY date) AS prev_price,
        RANK() OVER (PARTITION BY date, category ORDER BY final_price DESC) AS price_rank,
        ROUND((final_price - competitor_price) / competitor_price * 100, 2) AS price_gap_pct,
        ROUND(AVG(qty) OVER (
            PARTITION BY sku ORDER BY date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 2) AS ma7_qty
    FROM base
)
SELECT
    order_id, sku, date, category, season,
    final_price, cost, unit_profit,
    discount, competitor_price, price_gap_pct,
    inventory, qty AS sales, ma7_qty, price_rank,
    CASE
        WHEN prev_price IS NULL THEN NULL
        ELSE ROUND((final_price - prev_price) / prev_price * 100, 2)
    END AS price_change_pct
FROM enriched
WHERE qty IS NOT NULL;