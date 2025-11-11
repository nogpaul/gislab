# GISLab Portfolio

A professional GIS workspace for PostGIS, Python ETL, Remote Sensing, and Web GIS.

## Quickstart
1. Install prerequisites (see docs/winget-packages.json).
2. Create .env from .env.example and fill secrets.
3. Run: \setup/refresh-map.ps1\ to rebuild demo data and web map.
4. Serve the site: \cd web; python -m http.server 5500\.

## Repository Structure
- /data       : raw/source (not tracked), processed outputs
- /notebooks  : explorations
- /src        : Python packages & ETL scripts
- /web        : static web demo (Leaflet)
- /db         : SQL migrations and admin scripts
- /docs       : reports, runbooks, winget manifest
- /setup      : helper PowerShell scripts
- /envs       : Python virtual envs (ignored)

## What’s inside (Orientation)
- PostGIS database with sample data (places)
- Python ETL (psycopg/SQLAlchemy) CSV → PostGIS → GeoJSON
- Leaflet web map (search, filters, clustering)

## Next Steps
See \docs/NEXT_STEPS.md\ for the roadmap into DBMS, RS/EO, Python pipelines, Web GIS, and Analysis.
