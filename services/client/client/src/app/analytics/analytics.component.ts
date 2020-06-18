import {Component, OnInit} from '@angular/core';
import {delay, map} from 'rxjs/operators';
import {BreakpointObserver, Breakpoints} from '@angular/cdk/layout';
import {FtsQuery} from '../interfaces/fts-query';
import {FormControl} from '@angular/forms';
import {MatDatepickerInputEvent} from '@angular/material/datepicker';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { DomSanitizer } from '@angular/platform-browser';
import {Location} from '@angular/common';
import { timer } from 'rxjs';
@Component({
  selector: 'app-analytics',
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.scss']
})
export class AnalyticsComponent implements OnInit {

  wordCloudFiles = [
    'word_clouds1_Fri, 12 Jun 2020 23:48:35 GMT_0.png',
    'word_clouds1_Fri, 13 Mar 2020 23:48:35 GMT_0.png',
    'word_clouds1_Fri, 20 Mar 2020 23:48:35 GMT_0.png',
    'word_clouds1_Fri, 24 Apr 2020 23:48:35 GMT_0.png',
    'word_clouds1_Mon, 01 Jun 2020 23:48:35 GMT_0.png',
    'word_clouds1_Mon, 04 May 2020 23:48:35 GMT_0.png',
    'word_clouds1_Mon, 08 Jun 2020 23:48:35 GMT_0.png',
    'word_clouds1_Mon, 11 May 2020 23:48:35 GMT_0.png',
    'word_clouds1_Sat, 04 Apr 2020 23:48:35 GMT_0.png',
    'word_clouds1_Sat, 06 Jun 2020 23:48:35 GMT_0.png',
    'word_clouds1_Sat, 07 Mar 2020 23:48:35 GMT_0.png',
    'word_clouds1_Sat, 09 May 2020 23:48:35 GMT_0.png',
    'word_clouds1_Sat, 16 May 2020 23:48:35 GMT_0.png',
    'word_clouds1_Sat, 18 Apr 2020 23:48:35 GMT_0.png',
    'word_clouds1_Sat, 21 Mar 2020 23:48:35 GMT_0.png',
    'word_clouds1_Sat, 23 May 2020 23:48:35 GMT_0.png',
    'word_clouds1_Sat, 25 Apr 2020 23:48:35 GMT_0.png',
    'word_clouds1_Sun, 03 May 2020 23:48:35 GMT_0.png',
    'word_clouds1_Sun, 10 May 2020 23:48:35 GMT_0.png',
    'word_clouds1_Sun, 12 Apr 2020 23:48:35 GMT_0.png',
    'word_clouds1_Sun, 22 Mar 2020 23:48:35 GMT_0.png',
    'word_clouds1_Thu, 02 Apr 2020 23:48:35 GMT_0.png',
    'word_clouds1_Thu, 05 Mar 2020 23:48:35 GMT_0.png',
    'word_clouds1_Thu, 07 May 2020 23:48:35 GMT_0.png',
    'word_clouds1_Thu, 09 Apr 2020 23:48:35 GMT_0.png',
    'word_clouds1_Thu, 11 Jun 2020 23:48:35 GMT_0.png',
    'word_clouds1_Thu, 19 Mar 2020 23:48:35 GMT_0.png',
    'word_clouds1_Thu, 28 May 2020 23:48:35 GMT_0.png',
    'word_clouds1_Tue, 02 Jun 2020 23:48:35 GMT_0.png',
    'word_clouds1_Tue, 05 May 2020 23:48:35 GMT_0.png',
    'word_clouds1_Tue, 07 Apr 2020 23:48:35 GMT_0.png',
    'word_clouds1_Tue, 09 Jun 2020 23:48:35 GMT_0.png',
    'word_clouds1_Tue, 14 Apr 2020 23:48:35 GMT_0.png',
    'word_clouds1_Tue, 17 Mar 2020 23:48:35 GMT_0.png',
    'word_clouds1_Tue, 21 Apr 2020 23:48:35 GMT_0.png',
    'word_clouds1_Tue, 24 Mar 2020 23:48:35 GMT_0.png',
    'word_clouds1_Wed, 04 Mar 2020 23:48:35 GMT_0.png',
    'word_clouds1_Wed, 06 May 2020 23:48:35 GMT_0.png',
    'word_clouds1_Wed, 25 Mar 2020 23:48:35 GMT_0.png',
    'word_clouds1_Wed, 27 May 2020 23:48:35 GMT_0.png',

  ];

  diarisationFiles = [
  'chadaev_01_0312.png' ,
  'chadaev_02_0312.png' ,
  'darkshevych_01_3011.png' ,
  'dral_01_3011.png' ,
  'dral_02_3011.png' ,
  'fadeev_01_2811.png' ,
  'fadeev_01_2911.png' ,
  'fadeev_02_2811.png' ,
  'pavlychev_01_0412.png' ,
  'polyakov_01_3011.png' ,
  'popovich_01_0412.png' ,
  'raspopina_01_2811.png' ,
  'raspopina_01_2911.png' ,
  'raspopina_02_2911.png' ,
  'vorotnikov_01_0312.png' ,
  'vorotnikov_01_0412.png' ,
  'vorotnikov_02_0312.png' ,
  'vorotnikov_02_0412.png' ,
];
/*  thematicFiles = [
    'template.html' ,
    'template1.html' ,
    'template2.html' ,
    'template3.html' ,
  ];*/
  thematicFiles = [
    'template1.png' ,
    'template2.png' ,
    'template3.png' ,
  ];

  freqsFiles = [
    'freqs1.png' ,
    'freqs2.png' ,
    'freqs3.png' ,
    'freqs4.png' ,
    'freqs5.png' ,
    'freqs6.png' ,
    'freqs7.png' ,
  ];

  /** Based on the screen size, switch from standard to one column per row */
  cards = this.breakpointObserver.observe(Breakpoints.Handset).pipe(
    map(({matches}) => {
      if (matches) {
        return [
          {title: 'Card 1', cols: 1, rows: 1, frame: this.sanitizer.bypassSecurityTrustResourceUrl(this.thematicImage)},
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

  cloudImage: any;
  freqImage: any;
  diarisationImage: any;
  thematicImage: any;
  analysed = false;
  analyse() {
    if (!this.analysed ) {
      timer(1000).subscribe(x => {this.analysed = true; });
    } else {
      this.analysed = false;
      this.generateImageCloud();
      this.generateImageDiarisation();
      this.generateImageThematic();
      this.generateImageFreqs();
      this.analyse();
    }
  }


  getRandomElement(arr) {
    const randomIndex = Math.floor(Math.random() * arr.length);
    return arr[randomIndex];
  }

  generateImageCloud(): void {
    this.cloudImage = './assets/img/word_clouds/' + this.getRandomElement(this.wordCloudFiles);

  }

  generateImageDiarisation(): void {
    this.diarisationImage = './assets/img/diarisation/' + this.getRandomElement(this.diarisationFiles);
  }

  generateImageThematic(): void {
    this.thematicImage = './assets/img/thematics/' + this.getRandomElement(this.thematicFiles);
    // this.draw_html(this.thematicImage);
  }

  generateImageFreqs(): void {
    this.freqImage = './assets/img/freqs/' + this.getRandomElement(this.freqsFiles);
  }

//   draw_html(name): void {
//   //    XSS режет код
//   const headers = new HttpHeaders({
//     'Content-Type': 'text/plain',
//   });
//   this.http.get(name, {headers: headers, responseType: 'text'}).subscribe(data => {
//   // console.log(data.toString());
//   this.thematicImage = this.sanitizer.bypassSecurityTrustResourceUrl(name);
// });
// }



  dateChangedEvent(formNo: number, event: MatDatepickerInputEvent<Date>) {
    if (formNo === 0) {
      this.query.startDate = event.value;
    } else if (formNo === 1) {
      this.query.endDate = event.value;
    }
  }

  constructor(private breakpointObserver: BreakpointObserver,
              public http: HttpClient,
              public sanitizer: DomSanitizer,
              private location: Location
  ) {
    // console.log(sanitizer.bypassSecurityTrustHtml(this.template));
  }

  ngOnInit() {
    this.generateImageCloud();
    this.generateImageDiarisation();
    this.generateImageThematic();
    this.generateImageFreqs();
  }
}
