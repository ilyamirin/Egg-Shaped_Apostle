import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Place} from 'src/model/place.model';
import {environment} from '../environments/environment';
import {Observable} from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class PlaceService {

  /*exampleText = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Risus pretium quam vulputate dignissim. Eleifend donec pretium vulputate sapien nec sagittis aliquam malesuada. Hac habitasse platea dictumst vestibulum rhoncus est. Tristique senectus et netus et. At tempor commodo ullamcorper a lacus vestibulum. Dignissim suspendisse in est ante in nibh mauris cursus mattis. Sit amet purus gravida quis blandit. Massa id neque aliquam vestibulum. Convallis tellus id interdum velit laoreet.';

  places_dummy: Place[] = [
    (new Place()).deserialize({id: 1, seatNumber: 1, date: new Date(), text: this.exampleText}),
    (new Place()).deserialize({id: 2, seatNumber: 2, date: new Date(), text: this.exampleText}),
    (new Place()).deserialize({id: 3, seatNumber: 3, date: new Date(), text: this.exampleText})o
  ];*/

  places: Place[] = [];

  constructor(
    private http: HttpClient
  ) {
  }

  getByFilter(searchText: string, dateStart: Date, dateEnd: Date): Observable<any> {
    const query = {
      query: searchText,
      date_time_start: dateStart,
      date_time_end: dateEnd
    };

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': `${environment.apiURL}`,
    });

    const options = {headers};

    return this.http.post<any>(`${environment.apiURL}/fts`, query, options);
  }

  getById(id: number): Place {
    return this.places.find((el: Place) => el.id === id);
  }

}
