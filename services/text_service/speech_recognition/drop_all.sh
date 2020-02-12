sudo -u postgres bash -c : && RUNAS="sudo -u postgres"
$RUNAS bash<<_
dropdb text
dropuser administrators
dropuser services
dropuser text_service
