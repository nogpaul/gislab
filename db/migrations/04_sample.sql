-- 04_sample.sql
-- Simple places table with a geometry and a spatial index.
CREATE TABLE IF NOT EXISTS public.places (
  place_id   serial PRIMARY KEY,
  name       text NOT NULL,
  geom       geometry(Point, 4326) NOT NULL
);

INSERT INTO public.places (name, geom)
VALUES
  ('Town Hall', ST_SetSRID(ST_MakePoint(7.865, 51.497), 4326)),
  ('Station',   ST_SetSRID(ST_MakePoint(7.902, 51.492), 4326))
ON CONFLICT DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_places_geom ON public.places USING GIST (geom);

-- Grant read to readonly role; owner retains full rights.
GRANT USAGE ON SCHEMA public TO gislab_readonly;
GRANT SELECT ON public.places TO gislab_readonly;
