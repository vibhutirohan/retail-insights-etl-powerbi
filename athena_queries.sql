
-- Create external table
CREATE EXTERNAL TABLE IF NOT EXISTS retail_real_data (
  transaction_id STRING,
  date TIMESTAMP,
  customer_name STRING,
  product STRING,
  total_items INT,
  total_amount DOUBLE,
  payment_method STRING,
  store_location STRING,
  cashier_name STRING,
  customer_feedback STRING,
  discount_applied STRING,
  membership_status STRING,
  coupon_code_used STRING
)
STORED AS PARQUET
LOCATION 's3://your-bucket/processed/';

-- Sample Query
SELECT store_location, SUM(total_amount) AS total_sales
FROM retail_real_data
WHERE total_amount IS NOT NULL
GROUP BY store_location
ORDER BY total_sales DESC;
