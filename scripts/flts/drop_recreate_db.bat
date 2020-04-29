REM Drop/recreate database for testing STDM db configurations
echo off

SET DB_NAME=flts
SET PG_VERSION=11
SET PG_PORT=5801
SET PG_USER=postgres
SET SCRIPT_DIR="%USERPROFILE%\.qgis2\python\plugins\stdm\scripts\flts"

echo.
IF EXIST "C:\Program Files\PostgreSQL\%PG_VERSION%\bin\dropdb.exe" SET PSQL_DIR="C:\Program Files\PostgreSQL\%PG_VERSION%\bin\"
IF EXIST "C:\Program Files (x86)\PostgreSQL\%PG_VERSION%\bin\dropdb.exe" SET PSQL_DIR="C:\Program Files (x86)\PostgreSQL\%PG_VERSION%\bin\"
echo %PSQL_DIR%
cd /d %PSQL_DIR%
echo Attempting to delete %DB_NAME% database...
dropdb.exe --if-exists -h localhost -p %PG_PORT% -U %PG_USER% %DB_NAME%
echo Attempting to create %DB_NAME% database...
createdb.exe -O %PG_USER% -h localhost -p %PG_PORT% -U %PG_USER% %DB_NAME%
echo Attempting to create PostGIS extension...
psql.exe -h localhost -p %PG_PORT% -U %PG_USER% -d %DB_NAME% -c "CREATE EXTENSION postgis SCHEMA public VERSION \"2.5.2\""
cd %SCRIPT_DIR%
echo Done
