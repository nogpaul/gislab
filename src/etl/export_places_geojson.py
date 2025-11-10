# export_places_geojson.py
# Purpose: read places from PostGIS and produce a valid RFC 7946 GeoJSON file
# Output: C:\GISLab\web\data\places.geojson

import os, json
from pathlib import Path
from dotenv import load_dotenv
import psycopg

load_dotenv()  # loads .env with PGHOST/PORT/DB/USER/PASSWORD

OUTPATH = Path(r"C:\GISLab\web\data\places.geojson")

def main():
    # Build DSN; psycopg 3 uses modern, context-managed connections/cursors
    dsn = (
        f"host={os.getenv('PGHOST')} port={os.getenv('PGPORT')} "
        f"dbname={os.getenv('PGDATABASE')} user={os.getenv('PGUSER')} "
        f"password={os.getenv('PGPASSWORD')}"
    )

    # We’ll let PostgreSQL/PostGIS assemble correct RFC-7946 GeoJSON:
    # - ST_AsGeoJSON(geom, 6) → geometry JSON with up to 6 decimal places (compact for web maps)
    # - jsonb_build_object → FeatureCollection → features array
    # - to_jsonb(row) - 'geom' → properties without geometry column
    # NOTE: GeoJSON requires WGS84 lon/lat (EPSG:4326). If your table uses another SRID,
    # wrap geom: ST_AsGeoJSON(ST_Transform(geom,4326), 6).
    sql = """
    SELECT jsonb_build_object(
      'type','FeatureCollection',
      'features', COALESCE(jsonb_agg(
        jsonb_build_object(
          'type','Feature',
          'geometry', ST_AsGeoJSON(geom, 6)::jsonb,
          'properties', to_jsonb(row) - 'geom'
        )
      ), '[]'::jsonb)
    ) AS fc
    FROM (
      SELECT place_id, name, geom
      FROM public.places
      ORDER BY place_id
    ) AS row;
    """

    with psycopg.connect(dsn) as conn, conn.cursor() as cur:
        cur.execute(sql)
        fc = cur.fetchone()[0]  # a Python dict (via jsonb → psycopg)
        OUTPATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPATH.write_text(json.dumps(fc, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote {OUTPATH}")

if __name__ == "__main__":
    main()
