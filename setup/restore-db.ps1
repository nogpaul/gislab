param(
  [Parameter(Mandatory=\True)][string]\,
  [string]\ = 'gislab_restored'
)
# Drop target if exists, then restore
psql -U postgres -h localhost -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='\';" 2>
psql -U postgres -h localhost -c "DROP DATABASE IF EXISTS \;"
createdb -U postgres -h localhost \
pg_restore -U postgres -h localhost -d \ "\"
Write-Host "Restored to database: \"
