import {Component, OnInit} from '@angular/core';
import {FormControl, Validators} from '@angular/forms';
import {Place} from '../../model/place.model';
import {PlaceService, RecordService} from '../../service';
import {NbComponentStatus} from '@nebular/theme';
import {delay} from 'rxjs/operators';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  searchText: string;
  recognizedText: string;

  dateStart: Date;
  dateEnd: Date;

  places: Place[];

  placeNumbers: number[];

  placesForm: FormControl;
  recordTimeForm: FormControl;

  isRecognized: boolean;

  constructor(
    private placeService: PlaceService,
    private recordService: RecordService
  ) {
  }

  ngOnInit() {
    this.searchText = '';
    this.recognizedText = '';

    this.places = [];

    this.placeNumbers = [1, 2, 3, 4, 5, 6, 7, 8];

    this.placesForm = new FormControl();
    this.recordTimeForm = new FormControl('', [
      Validators.required,
      Validators.min(5),
      Validators.max(30)
    ]);

    this.isRecognized = true;
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

  recordTimeChecker(status: boolean): NbComponentStatus {
    return status ? 'danger' : 'basic';
  }

  record(time: number) {
    this.isRecognized = false;

    const ms = time * 1000;

    this.recordService.record(time).pipe(delay(ms)).subscribe(data => {
      this.isRecognized = true;
    });
  }

  recognize() {
    this.recordService.recognize().subscribe(data => {
      this.recognizedText = data;
    });
  }

}
