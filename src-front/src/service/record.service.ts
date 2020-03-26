import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {environment} from '../environments/environment';
import {Observable, of} from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class RecordService {

  constructor(
    private http: HttpClient
  ) {
  }

  record(time: number): Observable<any> {
    const params = {
      time
    };

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': `${environment.apiURL}`
    });

    const options = {headers};

    return this.http.post<any>(`${environment.apiURL}/record`, params, options);
  }

  recognize(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': `${environment.apiURL}`
    });

    const options = {headers};

    return this.http.get<any>(`${environment.apiURL}/recognize`, options);
  }

}
