-- Top 5 เมืองที่มี AQI สูงสุด
SELECT
    city,
    AVG(value) as avg_aqi
FROM aqi_data
GROUP BY city
ORDER BY avg_aqi DESC
LIMIT 5;

-- แนวโน้ม AQI รายเดือน
SELECT
    DATE_TRUNC('month', date) as month,
    AVG(value) as monthly_avg_aqi
FROM aqi_data
GROUP BY month
ORDER BY month;