SELECT
    DATE_FORMAT(created_at, 'yyyy-MM') AS month,
    ROUND(AVG(DATEDIFF(closed_at, created_at)), 2) AS avg_resolution_days
FROM issues
WHERE state = 'closed'
GROUP BY month
ORDER BY month
