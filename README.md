DE Homework 
ETL пайплайн який бере сирі CSV файли чистить ізавантажує в PostgreSQL через Docker

Файли з даними:
customers.csv
products.csv
orders.csv
order_items.csv

about code:

Пайплайн проходить 3 кроки
Extract-читає CSV файли
Transform-чистить дані(прибирає дублікати,видаляє пусті/биті значення,фіксить неправильні типи (дати, числа),фільтрує негативні значення і сміття)
Load-завантажує все в PostgreSQL(створює таблиці: dim_customers; dim_products; fact_orders; fact_order_items)

Як запустити
1. Запустити Docker: docker compose up -d
2. Перевірити що контейнер працює: docker ps
3. Запустити пайплайн: python main.py

Як зайти в базу
docker exec -it postgres_test psql -U admin -d test_db

Результат
Всередині psql: \dt

SELECT * FROM fact_orders LIMIT 10;
SELECT * FROM dim_customers LIMIT 10;
SELECT * FROM dim_products LIMIT 10;
SELECT * FROM fact_order_items LIMIT 10;
