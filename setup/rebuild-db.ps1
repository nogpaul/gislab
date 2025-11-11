param(
  [string]\ = 'gislab'
)
# Admin creds (prompt if not set)
if (-not \) {
  \ = Read-Host -AsSecureString 'Enter postgres superuser password' |
    ForEach-Object { (New-Object System.Net.NetworkCredential('', )).Password }
}
\    = 'postgres'
\    = 'localhost'
\    = '5432'

# 1) Drop and recreate
psql -v ON_ERROR_STOP=1 -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='\';" 2>
psql -v ON_ERROR_STOP=1 -c "DROP DATABASE IF EXISTS \;"
psql -v ON_ERROR_STOP=1 -c "DROP ROLE IF EXISTS gislab_readonly;"
psql -v ON_ERROR_STOP=1 -c "DROP ROLE IF EXISTS gislab;"

# 2) Re-run migrations 01.. (order matters)
psql -v ON_ERROR_STOP=1 -f "C:\GISLab\db\migrations\01_roles.sql"
psql -v ON_ERROR_STOP=1 -f "C:\GISLab\db\migrations\02_database.sql"
psql -v ON_ERROR_STOP=1 -d \ -f "C:\GISLab\db\migrations\03_postgis.sql"
psql -v ON_ERROR_STOP=1 -d \ -f "C:\GISLab\db\migrations\04_sample.sql"
psql -v ON_ERROR_STOP=1 -d \ -f "C:\GISLab\db\migrations\05_category.sql"

# 3) ETL + export
& "C:\GISLab\envs\gis311\Scripts\Activate.ps1"
python "C:\GISLab\src\etl\load_places_csv.py"
python "C:\GISLab\src\etl\export_places_geojson.py"
