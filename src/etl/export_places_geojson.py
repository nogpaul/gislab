import json
import os
from pathlib import Path

# Load .env if available
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

import psycopg

OUTPATH = Path(r"C:\GISLab\web\data\places.geojson")

SQL = """
-- Build a valid RFC 7946 FeatureCollection with category included
SELECT jsonb_build_object(
  'type','FeatureCollection',
  'features', COALESCE(jsonb_agg(
    jsonb_build_object(
      'type','Feature',
      -- Ensure WGS84 lon/lat and reasonable precision for web
      'geometry', ST_AsGeoJSON(
        CASE WHEN ST_SRID(geom) = 4326 THEN geom ELSE ST_Transform(geom,4326) END,
        6
      )::jsonb,
      -- Explicitly list properties so category is always present
      'properties', jsonb_build_object(
        'place_id', place_id,
        'name', name,
        'category', COALESCE(category, 'Other')
      )
    )
    ORDER BY place_id
  ), '[]'::jsonb)
) AS fc
FROM public.places;
"""


def main():
    dsn = (
        f"host={os.getenv('PGHOST', 'localhost')} "
        f"port={os.getenv('PGPORT', '5432')} "
        f"dbname={os.getenv('PGDATABASE', 'gislab')} "
        f"user={os.getenv('PGUSER', 'gislab')} "
        f"password={os.getenv('PGPASSWORD', '')}"
    )
    with psycopg.connect(dsn) as conn, conn.cursor() as cur:
        cur.execute(SQL)
        fc = cur.fetchone()[0]  # Python dict
        OUTPATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPATH.write_text(json.dumps(fc, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote {OUTPATH}")


if __name__ == "__main__":
    main()
