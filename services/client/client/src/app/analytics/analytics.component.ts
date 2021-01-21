import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {AnalyzeQuery} from '../interfaces/analyze-query';
import {Audio} from '../interfaces/audio';
import {MatDialog} from '@angular/material/dialog';
import {MatSort} from '@angular/material/sort';
import {PlayerComponent} from '../player/player.component';
import {AnalysisDialogueComponent} from '../analysis-dialogue/analysis-dialogue.component';
import {AudioplayerService} from '../services/audioplayer.service';
import {AudioService} from '../services/audio.service';
import {MatTableDataSource} from '@angular/material/table';
import {MatPaginator} from '@angular/material/paginator';
import {BehaviorSubject, timer} from 'rxjs';
import {FormControl} from '@angular/forms';
import {MatDatepickerInputEvent} from '@angular/material/datepicker';
import {PageTitle} from '../page-title/page-title';


@Component({
  selector: 'app-analytics',
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.scss']
})
export class AnalyticsComponent implements OnInit, AfterViewInit {

  query: AnalyzeQuery = {
  };

  resultsExist = false;

  workplaces = new FormControl();

  workplacesList: number[] = [0, 1, 2, 3, 4, 5, 6, 7, 8];

  template: any;
  records: BehaviorSubject<Audio[]> = new BehaviorSubject<Audio[]>([]);
  displayedColumns: string[] = ['id', 'name', 'year', 'month', 'day', 'hour', 'workplace', 'role'];
  dataSource: MatTableDataSource<Audio>;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  dateChangedEvent(formNo: number, event: MatDatepickerInputEvent<Date>) {
    if (formNo === 0) {
      this.query.date_time_start = event.value;
    } else if (formNo === 1) {
      this.query.date_time_end = event.value;
    }
  }

  getAudio(): void {
    this.recordsService.filterRecords(this.query)
      .subscribe(records => {
        // console.log(this.query)
        // console.log(this.query.work_places)
        records.map(x => {
          const date = new Date(Date.parse(x.date));
          // console.log(x)
          x.role = (x.role in [0, 1] ? (x.role.toString() === '0' ? 'Оператор' : 'Клиент') : 'Не указано');
          x.year = date.getFullYear();
          x.month = date.getMonth()+1;
          x.day = date.getDate();
          x.hour = date.getHours();
          x.minute = date.getMinutes();
          x.ms = date.getMilliseconds();
        });
        this.records.next(records);
        this.dataSource = new MatTableDataSource<Audio>(this.records.value);
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
        this.resultsExist = true;
      });
  }


  constructor(
    private audioService: AudioplayerService,
    private recordsService: AudioService,
    public dialog: MatDialog,
    public _pageTitle: PageTitle
  ) {
    this.dataSource = new MatTableDataSource();
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  ngOnInit(): void {
    this._pageTitle.title = 'Аналитика';
    this.getAudio();
  }

  analyse(id: string, index: number) {
    // console.log(id);
    const dialogRef = this.dialog.open(AnalysisDialogueComponent);
    dialogRef.componentInstance.file = id;
    // // dialogRef.componentInstance.openFile(id, index);
    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }
}
