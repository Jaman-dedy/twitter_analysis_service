import psycopg2
from app.config import settings

def create_test_database():
    conn = psycopg2.connect(
        dbname="postgres",
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_SERVER,
        port=settings.POSTGRES_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Check if the test database already exists
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{settings.POSTGRES_DB}_test'")
    exists = cursor.fetchone()
    
    if not exists:
        # Create the test database
        cursor.execute(f"CREATE DATABASE {settings.POSTGRES_DB}_test")
        print(f"Test database '{settings.POSTGRES_DB}_test' created successfully.")
    else:
        print(f"Test database '{settings.POSTGRES_DB}_test' already exists.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_test_database()