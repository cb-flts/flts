ECHO Populating FLTS tables
ECHO OFF
SET DB_NAME=flts
SET PG_VERSION=11
SET PG_PORT=5801
SET PG_USER=postgres
SET PG_HOST=localhost
SET SCRIPTS_DIR="%USERPROFILE%\.qgis2\python\plugins\stdm\scripts\flts\scripts\"
SET POPULATE="%USERPROFILE%\.qgis2\python\plugins\stdm\scripts\flts\scripts\populate.sql"
SET PSQL_DIR="C:\Program Files\PostgreSQL\%PG_VERSION%\bin\"
REM SET PSQL_DIR="C:\Program Files (x86)\PostgreSQL\%PG_VERSION%\bin\"
cd /d %PSQL_DIR%
ECHO Attempting to populate tables...
psql.exe -e -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -d %DB_NAME% -a -f %POPULATE%  > %SCRIPTS_DIR%\output.txt
DEL %SCRIPTS_DIR%\output.txt
cd %SCRIPTS_DIR%
ECHO Done
REM ------END--------
