import os
from dotenv import load_dotenv
import psycopg

load_dotenv()  # loads .env into process env

# Build a DSN (you could also use a URI string)
dsn = f"host={os.getenv('PGHOST')} port={os.getenv('PGPORT')} dbname={os.getenv('PGDATABASE')} user={os.getenv('PGUSER')} password={os.getenv('PGPASSWORD')}"

# Connections are context managers; commit/rollback handled explicitly
with psycopg.connect(dsn) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        print('PostgreSQL:', cur.fetchone()[0])
        cur.execute("SELECT PostGIS_Full_Version();")
        print('PostGIS:', cur.fetchone()[0])
