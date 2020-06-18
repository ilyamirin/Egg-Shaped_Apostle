import { Injectable } from '@angular/core';
import {Observable, of} from 'rxjs';
import {HttpParams, HttpHeaders, HttpClient} from '@angular/common/http';
import {catchError} from 'rxjs/operators';
import {FtsQuery} from '../interfaces/fts-query';

@Injectable({
  providedIn: 'root'
})
export class Ftsservice {
  private ftsServiceAPI = 'http://127.0.0.1:5727';

  httpOptions = {
    headers: [
      new HttpHeaders({'Content-Type': 'application/json'}),
      new HttpHeaders({'Access-Control-Allow-Origin': '*'})
    ]
  };

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      return of(result as T);
    };
  }


  search(query: FtsQuery): Observable<string> {
    let headers = new HttpHeaders().set('Access-Control-Allow-Origin', '*');
    return this.http.post<string>(this.ftsServiceAPI + '/fts', JSON.stringify(query), {headers: headers})
      .pipe(catchError(this.handleError<string>('record', ''))
      );
  }

  constructor(
    private http: HttpClient,
  ) {
  }
}
