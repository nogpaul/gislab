ALTER TABLE IF EXISTS public.places OWNER TO gislab;
DO ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO gislab_readonly;
BEGIN
  IF EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
             WHERE c.relname='places_place_id_seq' AND n.nspname='public') THEN
    ALTER SEQUENCE public.places_place_id_seq OWNER TO gislab;
  END IF;
ENDALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO gislab_readonly;;

GRANT ALL ON TABLE public.places TO gislab;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE public.places_place_id_seq TO gislab;

GRANT USAGE ON SCHEMA public TO gislab_readonly;
GRANT SELECT ON public.places TO gislab_readonly;
