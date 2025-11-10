import os, csv, sys, math
from pathlib import Path
from dotenv import load_dotenv
import psycopg
from psycopg import sql

load_dotenv()

CSV_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"C:\GISLab\data\raw\places.csv")

def valid_row(row):
    """Basic validation: non-empty name, finite lon/lat in range."""
    try:
        name = row["name"].strip()
        lon = float(row["lon"])
        lat = float(row["lat"])
        if not name:
            return False
        if not (math.isfinite(lon) and math.isfinite(lat)):
            return False
        if not (-180 <= lon <= 180 and -90 <= lat <= 90):
            return False
        return True
    except Exception:
        return False

def main():
    dsn = (
        f"host={os.getenv('PGHOST')} port={os.getenv('PGPORT')} "
        f"dbname={os.getenv('PGDATABASE')} user={os.getenv('PGUSER')} "
        f"password={os.getenv('PGPASSWORD')}"
    )

    with psycopg.connect(dsn, autocommit=False) as conn:
        with conn.cursor() as cur:
            # 1) Ensure table exists (same as Day 2 but safe to re-run)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS public.places (
              place_id   serial PRIMARY KEY,
              name       text NOT NULL,
              geom       geometry(Point, 4326) NOT NULL
            );
            """)
            # Unique key for idempotent upserts (names normalized)
            cur.execute("""
            DO $$
            BEGIN
              IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'ux_places_name_lower'
              ) THEN
                ALTER TABLE public.places
                ADD CONSTRAINT ux_places_name_lower UNIQUE (name);
              END IF;
            END$$;
            """)

            # 2) Create spatial index if missing
            cur.execute("""
            DO $$
            BEGIN
              IF NOT EXISTS (
                SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                WHERE c.relname = 'idx_places_geom' AND n.nspname = 'public'
              ) THEN
                CREATE INDEX idx_places_geom ON public.places USING GIST (geom);
              END IF;
            END$$;
            """)

            # 3) Read and clean CSV
            rows = []
            with open(CSV_PATH, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    if valid_row(r):
                        rows.append((r["name"].strip(), float(r["lon"]), float(r["lat"])))

            # 4) Upsert rows
            # Build geometry on the server: ST_SetSRID(ST_MakePoint(lon,lat),4326)
            upsert_sql = """
            INSERT INTO public.places (name, geom)
            VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
            ON CONFLICT (name)
            DO UPDATE SET geom = EXCLUDED.geom;
            """
            cur.executemany(upsert_sql, rows)

            # 5) Commit
            conn.commit()

            print(f"Upserted {len(rows)} rows into public.places")

if __name__ == "__main__":
    main()
