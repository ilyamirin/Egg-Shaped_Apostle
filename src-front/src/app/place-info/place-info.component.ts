import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Place} from '../../model/place.model';
import {PlaceService} from '../../service/place.service';


@Component({
  selector: 'place-info',
  templateUrl: './place-info.component.html',
  styleUrls: ['./place-info.component.scss']
})
export class PlaceInfoComponent implements OnInit {

  place: Place;

  constructor(
    private route: ActivatedRoute,
    private placeService: PlaceService
  ) {
  }

  ngOnInit() {
    const id = +this.route.snapshot.paramMap.get('id');

    this.placeService.getById(id).subscribe((data: Place) => {
      this.place = data;
    });
  }

}
