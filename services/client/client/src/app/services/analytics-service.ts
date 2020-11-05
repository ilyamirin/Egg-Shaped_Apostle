import {Injectable,} from '@angular/core';
import {HttpClient, HttpHeaders,} from '@angular/common/http';
import {Observable, of,} from 'rxjs';
import {catchError} from 'rxjs/operators';
import {Audio} from '../interfaces/audio';

class RequestOptions {
  constructor(param: { headers: Headers }) {

  }

}

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  private analyticsServiceAPI = 'http://127.0.0.1:5731';
  httpOptions = {
    headers: [
      // new HttpHeaders({'Content-Type': 'application/json'}),
      new HttpHeaders({'Access-Control-Allow-Origin': '*'})
    ]
  };

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      return of(result as T);
    };
  }

  getDiarizationPicture(audio: Audio): Observable<string> {
    console.log(audio.name);
    const headers = new HttpHeaders({
      'Access-Control-Allow-Origin': 'http://127.0.0.1:5731',
      Filename: audio.name
    });

    const options = { headers, responseType: 'text'};

    return this.http.get<any>(this.analyticsServiceAPI + '/svg/', options )
      .pipe(catchError(this.handleError<any>('getDiarizationPicture', ''))
      );

  }

  constructor(
    private http: HttpClient,
  ) {
  }


}

