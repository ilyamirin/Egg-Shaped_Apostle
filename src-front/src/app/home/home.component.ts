import {Component, OnInit} from '@angular/core';
import {Place} from '../../model/place.model';
import {PlaceService} from '../../service/place.service';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  searchText: string;

  dateStart: Date;

  dateEnd: Date;

  placeNumbers: number[];

  places: Place[];

  constructor(
    private placeService: PlaceService
  ) {
  }

  ngOnInit() {
    this.searchText = '';
    this.placeNumbers = [1, 2, 3, 4, 5, 6, 7, 8];
    this.places = [];
  }

  search() {
    this.places = this.placeService.getByFilter(this.searchText, this.dateStart, this.dateEnd);
  }

}
