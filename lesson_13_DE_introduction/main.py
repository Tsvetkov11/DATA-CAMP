import pandas as pd
from sqlalchemy import create_engine, text
import scripts.cleaning as clean

DB_URL = "postgresql://admin:password123@127.0.0.1:5433/test_db"
engine = create_engine(DB_URL)

def run_pipeline():
    print("extract")
    cust = pd.read_csv("lesson_13_DE_introduction/data/raw/customers.csv")
    prod = pd.read_csv("lesson_13_DE_introduction/data/raw/products.csv")
    ordr = pd.read_csv("lesson_13_DE_introduction/data/raw/orders.csv")
    item = pd.read_csv("lesson_13_DE_introduction/data/raw/order_items.csv")

    print("transform")
    cust_c = clean.clean_customers(cust)
    prod_c = clean.clean_products(prod)
    ordr_c = clean.clean_orders(ordr)
    item_c = clean.clean_order_items(item)

    print("load to docker")
    
    cust_c.to_sql("dim_customers", engine, if_exists="replace", index=False)
    prod_c.to_sql("dim_products", engine, if_exists="replace", index=False)
    ordr_c.to_sql("fact_orders", engine, if_exists="replace", index=False)
    item_c.to_sql("fact_order_items", engine, if_exists="replace", index=False)
    print("завантажено")

    print("SQL JOIN")
    query = """
    SELECT 
        c.customer_id, 
        SUM(i.quantity * p.price) as total_spent
    FROM dim_customers c
    JOIN fact_orders o ON c.customer_id = o.customer_id
    JOIN fact_order_items i ON o.order_id = i.order_id
    JOIN dim_products p ON i.product_id = p.product_id
    GROUP BY c.customer_id
    ORDER BY total_spent DESC;
    """
    
    with engine.connect() as conn:
        df_report = pd.read_sql(text(query), conn)
        df_report.to_csv("data/final_report.csv", index=False)
    
    print("file done")

if __name__ == "__main__":
    run_pipeline()