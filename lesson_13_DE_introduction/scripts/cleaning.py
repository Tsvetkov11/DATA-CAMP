import pandas as pd

def clean_customers(df):
    print("clean client")
    df = df.drop_duplicates(subset=[df.columns[0]], keep='last')
    return df

def clean_products(df):
    print("clean prod")
    # Очищаємо назви колонок, щоб не було помилок з регістрами
    df.columns = df.columns.str.strip().str.lower()
    
    # Шукаємо колонку з ID (перша колонка) та ціною
    id_col = df.columns[0]
    price_col = next((c for c in df.columns if 'price' in c), None)
    
    if price_col:
        df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
        df = df[df[price_col] > 0]
        
    df = df.drop_duplicates(subset=[id_col], keep='last')
    return df

def clean_orders(df):
    print("clean orders")
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(subset=[df.columns[0]])
    return df

def clean_order_items(df):
    print("clean or items")
    df.columns = df.columns.str.strip().str.lower()
    if 'quantity' in df.columns:
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').abs()
    return df