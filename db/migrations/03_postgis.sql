-- 03_postgis.sql
-- Enable PostGIS in the gislab DB and set search_path so postgis functions resolve nicely.
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_raster;

-- Optional but helpful so functions are found without schema prefixes in tools:
ALTER DATABASE gislab SET search_path = public, postgis;
