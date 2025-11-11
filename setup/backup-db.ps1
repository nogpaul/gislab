param([string]\ = 'gislab')
\ = Get-Date -Format 'yyyyMMdd_HHmmss'
\ = "C:\GISLab\db\backups\_\.dump"
# requires PGPASSWORD in env or .pgpass
pg_dump -Fc -d \ -h localhost -U postgres -f "\"
Write-Host "Backup written to: \"
