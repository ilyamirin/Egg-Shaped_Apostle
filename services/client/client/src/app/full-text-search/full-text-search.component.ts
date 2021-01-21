import {Component, OnInit} from '@angular/core';
import {MatDatepickerInputEvent} from '@angular/material/datepicker';
import {FormControl} from '@angular/forms';
import {FtsQuery} from '../interfaces/fts-query';
import {FtsResult} from '../interfaces/fts-result';
import {Ftsservice} from '../services/ftsservice';
import {PageTitle} from '../page-title/page-title';


@Component({
  selector: 'app-full-text-search',
  templateUrl: './full-text-search.component.html',
  styleUrls: ['./full-text-search.component.scss']
})
export class FullTextSearchComponent implements OnInit {
  query: FtsQuery = {
    text: '',
    startDate: new Date(Date.now() - 1000 * 60 * 60 * 24),
    endDate: new Date(Date.now()),
    role: -1,
    workplaces: []

  };
  results: FtsResult[];


  workplaces = new FormControl();

  workplacesList: number[] = [1, 2, 3, 4, 5, 6, 7, 8];

  search(query: FtsQuery): void {
    this.ftsService.search(this.query).subscribe(results => this.results = results);
  }

  mock_search(): void {
    this.query.text = 'привет';
    this.search(this.query);
  }

  truncateText(value: string, length: number): string {
    const elipses = '...';

    if (value.length <= length) {
      return value.replace(new RegExp(this.query.text, 'gi'), match => {
        return '<b>' + match + '</b>';
      });
    }

    if (length < elipses.length) {
      return '';
    }
    // console.log(new RegExp(this.query.text, 'gi'));
    const valueIndex = value.indexOf(this.query.text);
    console.log('valueInd: ', valueIndex);
    let leftBorder = Math.floor(valueIndex - length / 2);
    if (leftBorder < 0) {
      leftBorder = 0;
    }
    ;
    let rightBorder = Math.floor(valueIndex + length / 2);
    if (rightBorder > value.length) {
      rightBorder = value.length;
    }
    ;
    let truncatedText = value.slice(leftBorder, rightBorder);
    console.log('trunc:', truncatedText);
    while (truncatedText.length > length - elipses.length) {
      const lastSpace = truncatedText.lastIndexOf(' ');

      if (lastSpace === -1) {
        truncatedText = '';
        break;
      }

      truncatedText = truncatedText.slice(0, lastSpace).replace(/[!,.?]$/, '');
    }
    truncatedText = truncatedText.replace(new RegExp(this.query.text, 'gi'), match => {
      return '<b>' + match + '</b>';
    });
    return truncatedText + elipses;
  }

  dateChangedEvent(formNo: number, event: MatDatepickerInputEvent<Date>) {
    if (formNo === 0) {
      this.query.startDate = event.value;
    } else if (formNo === 1) {
      this.query.endDate = event.value;
    }
  }

  constructor(
    private ftsService: Ftsservice,
    public _pageTitle: PageTitle
  ) {
  }

  ngOnInit(): void {
    this._pageTitle.title = 'Поиск';
  }

}
