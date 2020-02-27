# for fts_service deploy:
## windows:
1. <code>python -m pip install flask virtualenv</code>
2. <code>cd ...\egg-shaped_apostle\services\fts_service</code>
3. <code>virtualenv flask</code>
4. Run Power Shell
<code>Invoke-WebRequest -Method POST -Uri http://localhost:5000/fts?work_place=0"&"role=1"&"date_time_start=2020-02-01"&"date_time_end=2020-02-28"&"query=\u0417\u0430\u043F\u0440\u043E\u0441\u0020\u043D\u0430\u0020\u043D\u0435\u0441\u043A\u043E\u043B\u044C\u043A\u043E\u0020\u0441\u0442\u0440\u043E\u043A"&"top=5 -Headers @{"Content-type"="application/json"}</code>
## ubuntu
1. <code>pip3 install flask virtualenv</code>
2. <code>cd ...\egg-shaped_apostle\services\fts_service</code>
3. <code>virtualenv flask</code>
4. Use curl for POST-query generation as indicated below:

REST API fts accepts the following parameters:
 - work_place=0 [0-8]
 - role=0 [0-1]
 - date_time_start=2020-02-01 [ISO 8601]
 - date_time_end=2020-02-28 [ISO 8601]
 - query="запрос на несколько фраз или предложений"
 - top=5 [ISO 8601]
 
e.g.:
<code>http://localhost:5000/fts?work_place=0&role=1&date_time_start=2020-02-01&date_time_end=2020-02-28&query=\u0417\u0430\u043F\u0440\u043E\u0441\u0020\u043D\u0430\u0020\u043D\u0435\u0441\u043A\u043E\u043B\u044C\u043A\u043E\u0020\u0441\u0442\u0440\u043E\u043A&top=5</code>
