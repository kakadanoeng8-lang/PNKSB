from database.connection import get_db_connection # កែសម្រួលទី១

def create_tables():
    conn = get_db_connection()
    if conn is None:
        return

    cursor = None # កែសម្រួលទី២: បង្កើតវាទុកមុនដើម្បីការពារកំហុស
    
    try:
        cursor = conn.cursor()
        
        # កូដ SQL សម្រាប់បញ្ជាឲ្យ PostgreSQL បង្កើតតារាង
        create_tables_sql = """
        -- ១. បង្កើតតារាងផលិតផល (Products Table)
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            barcode VARCHAR(100) UNIQUE,
            quantity INTEGER DEFAULT 0,
            price DECIMAL(10, 2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- ២. បង្កើតតារាងប្រវត្តិស្តុក (Stock Transactions Table)
        CREATE TABLE IF NOT EXISTS stock_transactions (
            id SERIAL PRIMARY KEY,
            product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
            transaction_type VARCHAR(4) CHECK (transaction_type IN ('IN', 'OUT')) NOT NULL, -- កែសម្រួលទី៣
            quantity INTEGER NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cursor.execute(create_tables_sql)
        conn.commit()
        print("🎉 បង្កើតតារាង products និង stock_transactions បានជោគជ័យ!")
        
    except Exception as e:
        print(f"❌ មានបញ្ហាក្នុងការបង្កើតតារាង: {e}")
        
    finally:
        # បិទការភ្ជាប់វិញដោយសុវត្ថិភាព
        if cursor: 
            cursor.close()
        if conn:
            conn.close()
            print("បិទការតភ្ជាប់វិញដោយសុវត្ថិភាព។")

if __name__ == "__main__":
    create_tables()