import { Injectable } from '@angular/core';
import { Observable, throwError, of } from 'rxjs';
import { catchError, map, tap} from 'rxjs/operators';
import {HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import {Audio} from '../interfaces/audio';
import {Microphone} from '../interfaces/microphone';

@Injectable({
  providedIn: 'root'
})
export class AudioService {
  private audioServiceAPI = 'http://192.168.0.1:5722';

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

  updateMicrophones(): Observable<Microphone[]> {
    return this.http.get<Microphone[]>(this.audioServiceAPI + '/raspberry/update')
      .pipe(catchError(this.handleError<Microphone[]>('updateMicrophones', []))
      );
  }

  record(rasp, card, name, time): Observable<string> {
    let params = new HttpParams().set('card', card);
    params = params.append('mic', name);
    params = params.append('time', time);
    const headers = new HttpHeaders({'Access-Control-Allow-Origin': '192.168.0.1:5722/raspberry/' + rasp + '/record'});
    return this.http.get<string>(this.audioServiceAPI + '/raspberry/' + rasp + '/record', {headers: headers, params: params})
      .pipe(catchError(this.handleError<string>('record', ''))
      );
  }

  constructor(
    private http: HttpClient,
  ) { }
}
