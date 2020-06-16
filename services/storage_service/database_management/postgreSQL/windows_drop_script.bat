@echo off
setlocal
set /p "PGPASSWORD=insert postgres password:"
cd "C:\Program Files\PostgreSQL\12\bin\"

dropdb -U postgres  text
echo database dropped...
dropuser -U postgres  administrators
dropuser -U postgres  services
dropuser -U postgres  text_service
echo users dropped...
endlocal

set /p=press any key to continue...

EXIT /B 0