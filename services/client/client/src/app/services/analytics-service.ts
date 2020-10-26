import { Injectable, } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import {Observable, of, throwError, } from 'rxjs';
import { catchError, map, tap} from 'rxjs/operators';
import {Audio} from '../interfaces/audio';
import { AnalyzeQuery } from '../interfaces/analyze-query';

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  private analyticsServiceAPI = 'http://127.0.0.1:5731';
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

  getDiarizationPicture(query: AnalyzeQuery): Observable<Audio[]> {
    const headers = new HttpHeaders().set('Access-Control-Allow-Origin', '*');
    return this.http.get<Audio[]>(this.analyticsServiceAPI + '/records')
      .pipe(catchError(this.handleError<Audio[]>('getRecords', []))
      );
  }

  constructor(
    private http: HttpClient,
) { }


}

