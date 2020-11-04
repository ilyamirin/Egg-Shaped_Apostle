#Analytics service
## Пока нет текста распознавания, выполняет только функцию диаризации
<ul>
<li>
<b>POST /analyse</b> будет принимать json-объект вида

```
'{"work_places": [0],
"roles": [0],
"date_time_start":
"2020-10-14T01:42:13.231691",
"date_time_end": "2020-10-14T02:15:13.231691"}'
```
, где обязательно должно быть json-тело, но ни один из параметров не является обязательным,
и возвращать json-объект вида

```
'{"response": [{"filename": "0_2_0_2020-10-14T02:53:51.796987.wav",
"role": 1,
"workplace": 1,
"diarization_markup": {разметка диаризации, см. /diarize},
"match scenario": 0.5,
"words_stat": {words: ["слово", ...], counts: [""]}
}
]}'
```
</li>
<li><b>POST /diarize</b> принимает запрос, содержащий заголовок "Content-Type: application/json" несущий в теле поля фильтрации, например

```
'{"work_places": [0],
"roles": [0],
"date_time_start":
"2020-10-14T01:42:13.231691",
"date_time_end": "2020-10-14T02:15:13.231691"}'
```
и возвращает json-объект следующего вида:


```
{response: {"имя файла": {
  "result": {
    "content": [
      {
        "label": "A", 
        "segment": {
          "end": 14.60365625, 
          "start": 1.2774687500000002
        }, 
        "track": "B"
      }, 
      {
        "label": "A", 
        "segment": {
          "end": 24.03003125, 
          "start": 20.72928125
        }, 
        "track": "C"
      }, 
      {
        "label": 1, 
        "segment": {
          "end": 27.25146875, 
          "start": 26.321656249999997
        }, 
        "track": "A"
      }
    ], 
    "modality": "speaker", 
    "pyannote": "Annotation"
  }
}
}}
```
curl:

```
curl -H "Content-Type: application/json" -d '{"work_places": [0], "roles": [0], "date_time_start": "2020-10-14T01:42:13.231691", "date_time_end": "2020-10-14T02:15:13.231691"}' 'http://127.0.0.1:5731/diarize'
```
####GET /svg
Curl:
```
curl -H "filename: 0_3_0_2020-09-08T04:16:14.336006.wav" http://127.0.0.1:5731/svg/
```
</li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
</ul>
