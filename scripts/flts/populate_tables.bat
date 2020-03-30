ECHO Populating FLTS tables
ECHO OFF
SET DB_NAME=flts
SET PG_VERSION=11
SET PG_PORT=5801
SET PG_USER=postgres
SET PG_HOST=localhost
SET POPULATE="%USERPROFILE%\.qgis2\python\plugins\stdm\scripts\flts\populate_relevant_authorities.sql"
SET FUNC="%USERPROFILE%\.qgis2\python\plugins\stdm\scripts\flts\landhold_certificate_utils.sql"
SET TRIGGER="%USERPROFILE%\.qgis2\python\plugins\stdm\scripts\flts\log_triggers.sql"
SET CERT_VW="%USERPROFILE%\.qgis2\python\plugins\stdm\scripts\flts\views\flts_cert_template_view.sql"
SET SCRIPT_DIR="%USERPROFILE%\.qgis2\python\plugins\stdm\scripts\flts"
SET PSQL_DIR="C:\Program Files\PostgreSQL\%PG_VERSION%\bin\"
REM SET PSQL_DIR="C:\Program Files (x86)\PostgreSQL\%PG_VERSION%\bin\"
cd /d %PSQL_DIR%
ECHO Attempting to populate tables...
psql.exe -e -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -d %DB_NAME% -a -f %POPULATE%  > %SCRIPT_DIR%\output.txt
psql.exe -e -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -d %DB_NAME% -a -f %FUNC%  > %SCRIPT_DIR%\output.txt
psql.exe -e -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -d %DB_NAME% -a -f %TRIGGER%  > %SCRIPT_DIR%\output.txt
psql.exe -e -h %PG_HOST% -p %PG_PORT% -U %PG_USER% -d %DB_NAME% -a -f %CERT_VW%  > %SCRIPT_DIR%\output.txt
DEL %SCRIPT_DIR%\output.txt
cd %SCRIPT_DIR%
ECHO Done
REM ------END--------
