import {Component, OnInit} from '@angular/core';
import {map} from 'rxjs/operators';
import {BreakpointObserver, Breakpoints} from '@angular/cdk/layout';
import {FtsQuery} from '../interfaces/fts-query';
import {FormControl} from '@angular/forms';
import {MatDatepickerInputEvent} from '@angular/material/datepicker';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-analytics',
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.scss']
})
export class AnalyticsComponent implements OnInit {
  /** Based on the screen size, switch from standard to one column per row */
  cards = this.breakpointObserver.observe(Breakpoints.Handset).pipe(
    map(({matches}) => {
      if (matches) {
        return [
          {title: 'Card 1', cols: 1, rows: 1, frame: this.sanitizer.bypassSecurityTrustResourceUrl('./assets/template.html')},
          {title: 'Card 4', cols: 1, rows: 1, frame: this.template},
          {title: 'Card 2', cols: 1, rows: 1, frame: this.template},
          {title: 'Card 3', cols: 1, rows: 1, frame: this.template}
        ];
      }

      return [
        {title: 'Card 1', cols: 1, rows: 1, frame: this.template},
        {title: 'Card 2', cols: 1, rows: 1, frame: this.template},
        {title: 'Card 3', cols: 1, rows: 1, frame: this.template},
        {title: 'Card 4', cols: 1, rows: 1, frame: this.template}
      ];
    })
  );

  // todo вынести в отдельные модули
  query: FtsQuery = {
    text: '',
    startDate: new Date(Date.now() - 1000 * 60 * 60 * 24),
    endDate: new Date(Date.now()),
    role: -1,
    workplaces: []

  };

  workplaces = new FormControl();

  workplacesList: number[] = [1, 2, 3, 4, 5, 6, 7, 8];

  template: any;

  dateChangedEvent(formNo: number, event: MatDatepickerInputEvent<Date>) {
    if (formNo === 0) {
      this.query.startDate = event.value;
    } else if (formNo === 1) {
      this.query.endDate = event.value;
    }
  }

  constructor(private breakpointObserver: BreakpointObserver,
              public http: HttpClient,
              public sanitizer: DomSanitizer) {
    // console.log(sanitizer.bypassSecurityTrustHtml(this.template));
  }

  ngOnInit() {
//    XSS режет код
    const headers = new HttpHeaders({
      'Content-Type': 'text/plain',
    });
    this.http.get('./assets/template.html', {headers: headers, responseType: 'text'}).subscribe(data => {
      console.log(data.toString());
      this.template = this.sanitizer.bypassSecurityTrustResourceUrl('./assets/template.html');
      console.log(this.template)
    });
  }
}
