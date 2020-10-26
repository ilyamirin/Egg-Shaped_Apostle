import { Component, OnInit } from '@angular/core';
import { AnalyticsService } from '../services/analytics-service';

@Component({
  selector: 'app-analysis-dialogue',
  templateUrl: './analysis-dialogue.component.html',
  styleUrls: ['./analysis-dialogue.component.scss']
})
export class AnalysisDialogueComponent implements OnInit {
  public files: Array<any> = [];
  constructor(
    public analyticsService: AnalyticsService
  ) { }

  ngOnInit(): void {
  }

}
