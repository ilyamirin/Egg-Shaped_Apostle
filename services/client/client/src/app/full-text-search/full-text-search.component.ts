import { Component, OnInit } from '@angular/core';
import {MatDatepickerInputEvent} from '@angular/material/datepicker';
import {FormControl} from '@angular/forms';
import {stringify} from 'querystring';
import {FtsQuery} from '../interfaces/fts-query';

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

  workplaces = new FormControl();

  workplacesList: number[] = [1, 2, 3, 4, 5, 6, 7, 8];

  dateChangedEvent(formNo: number, event: MatDatepickerInputEvent<Date>) {
    if (formNo === 0) {
      this.query.startDate = event.value;
    } else if (formNo === 1) {
      this.query.endDate = event.value;
    }
  }



  constructor() { }
  ngOnInit(): void {
  }

}
