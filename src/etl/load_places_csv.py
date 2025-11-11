import csv
import os
import re
import sys
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = (
    Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"C:\GISLab\data\raw\places.csv")
)


def valid_row(row):
    """Basic validation: non-empty name, finite lon/lat in range."""
    try:
        name = row["name"].strip()
        lon = float(row["lon"])
        lat = float(row["lat"])
        return bool(name) and -180 <= lon <= 180 and -90 <= lat <= 90
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
            # Ensure table exists (add category column if missing)
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS public.places (
              place_id serial PRIMARY KEY,
              name     text NOT NULL UNIQUE,
              geom     geometry(Point,4326) NOT NULL,
              category text
            );
            """
            )

            # Spatial index
            cur.execute(
                """
            DO $$
            BEGIN
              IF NOT EXISTS (
                SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                WHERE c.relname = 'idx_places_geom' AND n.nspname = 'public'
              ) THEN
                CREATE INDEX idx_places_geom ON public.places USING GIST (geom);
              END IF;
            END$$;
            """
            )

            # 3) Read and clean CSV

            def normalize_category(val: str | None) -> str | None:
                if not val:
                    return None
                # collapse internal whitespace + trim
                v = re.sub(r"\s+", " ", val).strip()
                if not v:
                    return None
                # normalize common spellings to a canonical form
                synonyms = {
                    "residential apparment": "Residential Appartment",
                    "gas station": "Gas Station",
                    "grocery shop": "Grocery Shop",
                }
                key = v.lower()
                return synonyms.get(key, v)  # keep original casing if not mapped

            rows = []
            with open(CSV_PATH, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    if valid_row(r):
                        name = r["name"].strip()
                        lon = float(r["lon"])
                        lat = float(r["lat"])
                        category = normalize_category(r.get("category"))
                        rows.append((name, lon, lat, category))

            upsert_sql = """
            INSERT INTO public.places (name, geom, category)
            VALUES (%s, ST_SetSRID(ST_MakePoint(%s,%s),4326), %s)
            ON CONFLICT (name) DO UPDATE
            SET geom = EXCLUDED.geom,
              category = COALESCE(EXCLUDED.category, public.places.category);
            """
            cur.executemany(upsert_sql, rows)
            conn.commit()
            print(f"Upserted {len(rows)} rows into public.places")


if __name__ == "__main__":
    main()
