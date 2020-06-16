@echo off
for /f "delims=" %%a in ('dir /s /b postgresql*.exe') do set "file_name=%%a"

setlocal
:PROMPT
SET /P INSTALL=Install PostgreSQL? (Y/[N])?
IF /I %INSTALL% NEQ Y GOTO create_db


:install

set /p "PGPASSWORD=insert postgres password:"
set /p "sec_pass=insert password again:"

if %PGPASSWORD%==%sec_pass% (%file_name% --optionfile config_param --superpassword %PGPASSWORD%) else (echo input passwords are not match)


:create_db

IF /I %INSTALL% NEQ Y (set /p "PGPASSWORD=insert postgres password:")

cd "C:\Program Files\PostgreSQL\12\bin\"
echo creating administrators role...
createuser.exe -U postgres -d -r -P administrators
echo creating services role...
createuser.exe -U postgres -P services
echo creating text_service role...
createuser.exe -U postgres -g services -P text_service
createdb.exe -U postgres text
psql.exe -U postgres text < %~dp0/create_data_structure.sql

endlocal

set /p=press any key to continue...

EXIT /B 0