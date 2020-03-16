ECHO Populating FLTS tables
ECHO OFF
SET DB_NAME=flts
SET PG_VERSION=11
SET PG_PORT=5801
SET PG_USER=postgres
SET PG_HOST=localhost
SET SCR_ONE="%USERPROFILE%\.qgis2\python\plugins\stdm\scripts\flts\custom_functions.sql"
SET SCR_TWO="%USERPROFILE%\.qgis2\python\plugins\stdm\scripts\flts\populate_tables.sql"
SET STDM_HOME="%USERPROFILE%\.qgis2\python\plugins\stdm"
SET PSQL_DIR="C:\Program Files\PostgreSQL\%PG_VERSION%\bin\"
REM SET PSQL_DIR="C:\Program Files (x86)\PostgreSQL\%PG_VERSION%\bin\"
cd /d %PSQL_DIR%
ECHO Attempting to populate tables...
psql.exe -e -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -d %DB_NAME% -a -f %SCR_ONE%  > %STDM_HOME%\output.txt
psql.exe -e -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -d %DB_NAME% -a -f %SCR_TWO%  > %STDM_HOME%\output.txt
DEL %STDM_HOME%\output.txt
cd %STDM_HOME%
ECHO Done
