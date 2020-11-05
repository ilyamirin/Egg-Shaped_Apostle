import {Component, OnInit} from '@angular/core';
import {AnalyticsService} from '../services/analytics-service';
import {DomSanitizer} from '@angular/platform-browser';
import {Observable} from 'rxjs';


@Component({
  selector: 'app-analysis-dialogue',
  templateUrl: './analysis-dialogue.component.html',
  styleUrls: ['./analysis-dialogue.component.scss']
})
export class AnalysisDialogueComponent implements OnInit {
  public file: any = {};
  diarSvg: string;

  constructor(
    public sanitizer: DomSanitizer,
    public analyticsService: AnalyticsService
  ) {
  }

  ngOnInit(): void {
    this.analyticsService.getDiarizationPicture(this.file).subscribe(svg => {
      this.diarSvg = svg;
      // console.log('result of request: ', svg)
    })
    // console.log(this.diarSvg+ '!!!!!');
  }

}
