from database.connection import get_db_connection

# ១. មុខងារសម្រាប់ទាញយកផលិតផល (Read)
def get_all_products():
    conn = get_db_connection()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor()
        # ទាញយក ឈ្មោះ, ចំនួន និងតម្លៃ ពីតារាង products
        cursor.execute("SELECT name, quantity, price FROM products;")
        products = cursor.fetchall()
        return products
    except Exception as e:
        print(f"❌ កំហុសក្នុងការទាញយកទិន្នន័យ: {e}")
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()

# ២. មុខងារសម្រាប់បញ្ចូលផលិតផលថ្មី (Insert)
def add_product(name, barcode, price, quantity=0):
    conn = get_db_connection()
    if conn is None:
        return False
        
    try:
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO products (name, barcode, price, quantity) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name, barcode, price, quantity))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ កំហុសក្នុងការបញ្ចូលទិន្នន័យ: {e}")
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()