# Instructions and scripts for fast postgreSQL DB deploying
## for windows:
1) Go to https://www.enterprisedb.com/downloads/postgres-postgresql-downloads;
2) Download the latest version (checked on 12.2);
3) Run downloaded installation executable, and place it in current directory;
4) Run <b>windows_deploy_script.bat</b>, add passwords (unsecure, make sure that no one is standing behind you:) for postgre and all additional roles.

## for POSIX:
1) Install postgreSQL with your package manager, i.e. for ubuntu <code>#sudo apt-get install postgresql postgresql-contrib</code>;
2) run <b>posix_deploy_script.sh</b>.