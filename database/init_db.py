from connection import get_db_connection

def create_tables():
    # ហៅទូរស័ព្ទទៅភ្ជាប់ជាមួយ Database ដោយប្រើ function ពីឯកសារ connection.py
    conn = get_db_connection()
    if conn is None:
        return

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
            transaction_type VARCHAR(10) NOT NULL, -- ដាក់បានតែពាក្យ 'IN' ឬ 'OUT'
            quantity INTEGER NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # បញ្ជាឲ្យដំណើរការកូដ SQL ខាងលើ
        cursor.execute(create_tables_sql)
        
        # Save ការផ្លាស់ប្តូរទៅកាន់ Database
        conn.commit()
        
        print("🎉 បង្កើតតារាង products និង stock_transactions បានជោគជ័យ!")
        
    except Exception as e:
        print(f"❌ មានបញ្ហាក្នុងការបង្កើតតារាង: {e}")
        
    finally:
        # បិទការភ្ជាប់វិញ ក្រោយពេលធ្វើការងារចប់ ដើម្បីកុំឲ្យធ្ងន់ម៉ាស៊ីន
        if conn:
            cursor.close()
            conn.close()
            print("បិទការតភ្ជាប់វិញដោយសុវត្ថិភាព។")

# បញ្ជាឲ្យមុខងារនេះដើរនៅពេលយើង Run ឯកសារនេះ
if __name__ == "__main__":
    create_tables()