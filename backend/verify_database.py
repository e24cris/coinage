from app import create_app, db
from sqlalchemy import inspect

def verify_database():
    """
    Verify database tables and their structure
    """
    app = create_app()
    
    with app.app_context():
        # Get inspector
        inspector = inspect(db.engine)
        
        # List all tables
        print("🔍 Database Tables:")
        tables = inspector.get_table_names()
        for table in tables:
            print(f"📋 Table: {table}")
            
            # Get columns for each table
            columns = inspector.get_columns(table)
            print("   Columns:")
            for column in columns:
                print(f"   - {column['name']}: {column['type']}")
            print()

if __name__ == '__main__':
    verify_database()
