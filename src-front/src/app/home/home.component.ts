import {Component, OnInit} from '@angular/core';
import {Place} from '../../model/place.model';
import {PlaceService} from '../../service/place.service';
import {FormControl} from '@angular/forms';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  searchText: string;

  dateStart: Date;
  dateEnd: Date;

  places: Place[];

  placesForm: FormControl;

  constructor(
    private placeService: PlaceService
  ) {
  }

  ngOnInit() {
    this.searchText = '';

    this.places = [];

    this.placesForm = new FormControl();
  }

  search() {
    this.placeService.getByFilter(this.searchText, this.dateStart, this.dateEnd, this.placesForm.value).subscribe(data => {
      const cards = data.search_results;

      this.places = [];

      for (const card of cards) {
        this.places.push((new Place()).deserialize({
          id: card.id,
          seatNumber: card.work_place,
          date: new Date(card.date_time),
          text: card.text
        }));
      }
    });
  }

}
