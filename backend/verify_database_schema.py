import os
import sys
from sqlalchemy import inspect

# Ensure backend directory is in Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_database_schema():
    """
    Comprehensive database schema verification
    """
    try:
        from app import create_app, db
        from sqlalchemy import inspect

        # Create Flask application context
        app = create_app()

        with app.app_context():
            print("🔍 Database Schema Verification")
            print("-------------------------------")

            # Use SQLAlchemy inspector
            inspector = inspect(db.engine)
            
            # Get all table names
            tables = inspector.get_table_names()
            
            print("\n📊 Database Tables:")
            for table in tables:
                print(f"\n🔹 Table: {table}")
                
                # Get column information
                columns = inspector.get_columns(table)
                print("   Columns:")
                for column in columns:
                    col_type = str(column['type'])
                    nullable = "Nullable" if column['nullable'] else "Not Nullable"
                    primary_key = "Primary Key" if column.get('primary_key', False) else ""
                    
                    print(f"   - {column['name']}: {col_type} ({nullable}) {primary_key}")
                
                # Get foreign key constraints
                try:
                    foreign_keys = inspector.get_foreign_keys(table)
                    if foreign_keys:
                        print("   Foreign Keys:")
                        for fk in foreign_keys:
                            print(f"   - {fk['name']}: {fk['constrained_columns']} → {fk['referred_table']}")
                except Exception as fk_error:
                    print(f"   ❌ Error retrieving foreign keys: {fk_error}")

            print(f"\n✅ Schema Verification Complete!")
            print(f"   Total Tables: {len(tables)}")

    except Exception as e:
        print(f"❌ Database Schema Verification Failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """
    Main entry point for database schema verification
    """
    verify_database_schema()

if __name__ == '__main__':
    main()
