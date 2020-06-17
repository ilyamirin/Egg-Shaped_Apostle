import { Injectable } from '@angular/core';
import { Observable, throwError, of } from 'rxjs';
import { catchError, map, tap} from 'rxjs/operators';
import { HttpClient, HttpHeaders, } from '@angular/common/http';

import {Audio} from '../interfaces/audio';
import {Microphone} from '../interfaces/microphone';

@Injectable({
  providedIn: 'root'
})
export class AudioService {
  private audioServiceAPI = 'http://127.0.0.1:5722';

  httpOptions = {
    headers: [
      new HttpHeaders({'Content-Type': 'application/json'}),
      new HttpHeaders({'Access-Control-Allow-Origin': '127.0.0.1:5722'})
    ]
  };


  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      return of(result as T);
    };
  }

  getRecords(): Observable<Audio[]> {
    return this.http.get<Audio[]>(this.audioServiceAPI + '/records')
      .pipe(catchError(this.handleError<Audio[]>('getRecords', []))
);
}

  getMicrophones(): Observable<Microphone[]> {
    return this.http.get<Microphone[]>(this.audioServiceAPI + '/microphones')
      .pipe(catchError(this.handleError<Microphone[]>('getMicrophones', []))
      );
  }

  constructor(
    private http: HttpClient,
  ) { }
}
