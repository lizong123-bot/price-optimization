WITH stats AS (
    SELECT
        category,
        AVG(final_price) AS avg_p,
        SQRT(AVG(final_price * final_price) - AVG(final_price) * AVG(final_price)) AS std_p
    FROM (
        SELECT p.category, s.price * (1 - s.discount) AS final_price
        FROM sales s JOIN product p ON s.sku = p.sku
    ) GROUP BY category
)
SELECT b.sku, b.category, b.final_price, st.avg_p, st.std_p,
       ROUND((b.final_price - st.avg_p) / st.std_p, 2) AS z_score
FROM (
    SELECT p.category, s.sku, s.price * (1 - s.discount) AS final_price
    FROM sales s JOIN product p ON s.sku = p.sku
) b
JOIN stats st ON b.category = st.category
WHERE ABS((b.final_price - st.avg_p) / st.std_p) > 3;