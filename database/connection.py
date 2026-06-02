import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        print("✅ ភ្ជាប់ទៅកាន់ PostgreSQL Database ជោគជ័យ!")
        return conn
    except Exception as e:
        print(f"❌ មានបញ្ហាក្នុងការភ្ជាប់ Database: {e}")
        return None

if __name__ == "__main__":
    test_conn = get_db_connection()
    if test_conn:
        test_conn.close()