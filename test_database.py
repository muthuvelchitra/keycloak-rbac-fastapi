from sqlalchemy import text

from app.database import engine, Base
from app.models import User


try:

    # Create tables
    Base.metadata.create_all(bind=engine)

    print("Database connection successful!")
    print("Users table created successfully!")

    # Verify table
    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'users';
            """)
        )

        table = result.fetchone()

        if table:
            print("Verified: users table exists.")
        else:
            print("users table not found.")


except Exception as e:

    print("Database operation failed!")
    print(e)