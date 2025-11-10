-- 01_roles.sql
-- Create a dedicated application owner and a readonly role.
-- Edit the password before running; never commit real secrets.
CREATE ROLE gislab WITH LOGIN PASSWORD 'CHANGE_ME' NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
CREATE ROLE gislab_readonly NOLOGIN;
