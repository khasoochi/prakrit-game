#!/usr/bin/env python3
"""
Upload SQLite databases to Turso.
Migrates verb_forms.db and noun_forms.db to Turso cloud database.
"""

import os
import sqlite3
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from libsql_client import create_client
except ImportError:
    print("❌ libsql-client not installed")
    print("Install with: pip install libsql-client")
    sys.exit(1)


def get_sqlite_schema(db_path):
    """Get CREATE TABLE statements from SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sql FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
    """)

    schemas = [row[0] for row in cursor.fetchall() if row[0]]
    conn.close()
    return schemas


def get_table_data(db_path, table_name):
    """Get all data from a table."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    columns = rows[0].keys() if rows else []
    data = [dict(row) for row in rows]

    conn.close()
    return columns, data


def get_table_names(db_path):
    """Get all table names from SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
    """)

    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables


def upload_database(turso_client, db_path, db_name):
    """Upload entire SQLite database to Turso."""
    print(f"\n{'='*60}")
    print(f"Uploading {db_name} to Turso")
    print(f"{'='*60}\n")

    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False

    try:
        # Get and create tables
        print("📋 Creating tables...")
        schemas = get_sqlite_schema(db_path)

        for schema in schemas:
            print(f"  Creating table...")
            # Drop table if exists (for re-running)
            table_name = schema.split()[2]  # Extract table name from CREATE TABLE
            try:
                turso_client.execute(f"DROP TABLE IF EXISTS {table_name}")
            except:
                pass

            turso_client.execute(schema)
            print(f"  ✓ Created table: {table_name}")

        # Get and insert data
        print("\n📦 Inserting data...")
        tables = get_table_names(db_path)

        for table in tables:
            if table == 'sqlite_sequence':
                continue

            columns, data = get_table_data(db_path, table)

            if not data:
                print(f"  ⚠️ No data in {table}")
                continue

            print(f"  Inserting {len(data)} rows into {table}...")

            # Batch insert for efficiency
            placeholders = ','.join(['?' for _ in columns])
            insert_sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"

            batch_size = 100
            for i in range(0, len(data), batch_size):
                batch = data[i:i+batch_size]
                for row_data in batch:
                    values = tuple(row_data[col] for col in columns)
                    turso_client.execute(insert_sql, values)

                print(f"    Progress: {min(i+batch_size, len(data))}/{len(data)} rows")

            print(f"  ✓ Inserted {len(data)} rows into {table}")

        print(f"\n✓ Successfully uploaded {db_name}!")
        return True

    except Exception as e:
        print(f"\n❌ Error uploading {db_name}: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_upload(turso_client):
    """Verify data was uploaded correctly."""
    print(f"\n{'='*60}")
    print("Verifying Upload")
    print(f"{'='*60}\n")

    try:
        # Check tables
        tables_query = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """
        result = turso_client.execute(tables_query)

        print("📊 Tables found:")
        tables = [row[0] for row in result.rows] if result.rows else []
        for table in tables:
            print(f"  - {table}")

        # Count records
        print("\n📈 Record counts:")
        for table in tables:
            result = turso_client.execute(f"SELECT COUNT(*) FROM {table}")
            count = result.rows[0][0] if result.rows else 0
            print(f"  {table}: {count} rows")

        print("\n✓ Verification complete!")
        return True

    except Exception as e:
        print(f"\n❌ Error verifying upload: {e}")
        return False


def main():
    """Main upload process."""
    print("\n🚀 Turso Database Upload Tool")
    print("="*60)

    # Load environment variables
    load_dotenv()

    turso_url = os.getenv('TURSO_DATABASE_URL')
    turso_token = os.getenv('TURSO_AUTH_TOKEN')

    if not turso_url or not turso_token:
        print("\n❌ Missing Turso credentials!")
        print("Set TURSO_DATABASE_URL and TURSO_AUTH_TOKEN in .env file")
        print("\nExample .env:")
        print("  TURSO_DATABASE_URL=libsql://your-db.turso.io")
        print("  TURSO_AUTH_TOKEN=your_token_here")
        sys.exit(1)

    print(f"\n✓ Turso URL: {turso_url}")
    print(f"✓ Token: {turso_token[:20]}...")

    # Connect to Turso
    print("\n🔌 Connecting to Turso...")
    try:
        turso_client = create_client(url=turso_url, auth_token=turso_token)
        print("✓ Connected to Turso!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)

    # Get database paths
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'

    verb_db = data_dir / 'verb_forms.db'
    noun_db = data_dir / 'noun_forms.db'

    # Upload databases
    print("\n" + "="*60)
    print("Starting Upload Process")
    print("="*60)

    success = True

    # Upload verb database
    if verb_db.exists():
        if not upload_database(turso_client, str(verb_db), 'verb_forms.db'):
            success = False
    else:
        print(f"⚠️ Verb database not found: {verb_db}")

    # Upload noun database
    if noun_db.exists():
        if not upload_database(turso_client, str(noun_db), 'noun_forms.db'):
            success = False
    else:
        print(f"⚠️ Noun database not found: {noun_db}")

    # Verify upload
    if success:
        verify_upload(turso_client)

    # Close connection
    try:
        turso_client.close()
    except:
        pass

    if success:
        print("\n" + "="*60)
        print("✅ UPLOAD COMPLETE!")
        print("="*60)
        print("\nYour Prakrit databases are now on Turso!")
        print("You can now deploy your web app to Vercel.")
        print("\nNext steps:")
        print("1. Test locally: streamlit run streamlit_app.py")
        print("2. Deploy to Vercel with your Turso credentials")
    else:
        print("\n❌ Upload had errors. Please check the output above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
