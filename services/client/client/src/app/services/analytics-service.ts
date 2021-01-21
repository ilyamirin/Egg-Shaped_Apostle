import {Injectable,} from '@angular/core';
import {HttpClient, HttpHeaders,} from '@angular/common/http';
import {Observable, of,} from 'rxjs';
import {catchError} from 'rxjs/operators';
import {Audio} from '../interfaces/audio';
import {environment} from '../../environments/environment';

class RequestOptions {
  constructor(param: { headers: Headers }) {

  }

}

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
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
      'Access-Control-Allow-Origin': environment.analyticsServiceAPI,
      Filename: audio.name
    });

    const options = {headers, responseType: 'text'};

    // FIXME: "options" make the app crash
    /*return this.http.get<any>(environment.analyticsServiceAPI + '/svg/', options )
      .pipe(catchError(this.handleError<any>('getDiarizationPicture', ''))
      );*/

    return this.http.get<any>(environment.analyticsServiceAPI + '/svg/')
      .pipe(catchError(this.handleError<any>('getDiarizationPicture', ''))
      );

  }

  constructor(
    private http: HttpClient,
  ) {
  }


}

