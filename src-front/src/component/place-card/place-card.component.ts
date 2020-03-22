import {Component, Input, OnInit} from '@angular/core';
import {Place} from '../../model/place.model';


@Component({
  selector: 'place-card',
  templateUrl: './place-card.component.html',
  styleUrls: ['./place-card.component.scss']
})
export class PlaceCardComponent implements OnInit {

  @Input()
  place: Place;

  @Input()
  isFullText: boolean;

  @Input()
  searchText: string | null;

  constructor() {
  }

  ngOnInit() {
    this.isFullText = true;

    if (!this.isFullText) {
      this.place.text = this.trancateText(this.place.text, 100);
    }

    if (this.searchText) {
      this.place.text = this.place.text.replace(new RegExp(this.searchText, 'gi'), match => {
        return '<b>' + match + '</b>';
      });
    }
  }

  trancateText(value: string, length: number): string {
    const elipses = '...';

    if (value.length <= length) {
      return value;
    }

    if (length < elipses.length) {
      return '';
    }

    let truncatedText = value.slice(0, length);

    while (truncatedText.length > length - elipses.length) {
      const lastSpace = truncatedText.lastIndexOf(' ');

      if (lastSpace === -1) {
        truncatedText = '';
        break;
      }

      truncatedText = truncatedText.slice(0, lastSpace).replace(/[!,.?]$/, '');
    }

    return truncatedText + elipses;
  }

}
