import { Injectable } from '@angular/core';
import {Observable, of} from 'rxjs';
import {HttpParams, HttpHeaders, HttpClient} from '@angular/common/http';
import {catchError} from 'rxjs/operators';
import {FtsQuery} from '../interfaces/fts-query';
import {FtsResult} from '../interfaces/fts-result';

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

  search(query: FtsQuery): Observable<FtsResult[]> {
    const headers = new HttpHeaders().set('Access-Control-Allow-Origin', '*');
    console.log(JSON.stringify(query));
    return this.http.post<FtsResult[]>(this.ftsServiceAPI + '/fts', query, {headers})
      .pipe(catchError(this.handleError<FtsResult[]>('getResults', []))
      );
  }

  constructor(
    private http: HttpClient,
  ) {
  }
}
