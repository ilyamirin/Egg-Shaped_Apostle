import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {FtsQuery} from '../interfaces/fts-query';
import {Audio} from '../interfaces/audio';
import {MatDialog} from '@angular/material/dialog';
import {MatSort} from '@angular/material/sort';
import {PlayerComponent} from '../player/player.component';
import {AudioplayerService} from '../services/audioplayer.service';
import {AudioService} from '../services/audio.service';
import {MatTableDataSource} from '@angular/material/table';
import {MatPaginator} from '@angular/material/paginator';
import {BehaviorSubject, timer} from 'rxjs';
import {FormControl} from '@angular/forms';


@Component({
  selector: 'app-analytics',
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.scss']
})
export class AnalyticsComponent implements OnInit, AfterViewInit {

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
  records: BehaviorSubject<Audio[]> = new BehaviorSubject<Audio[]>([]);
  displayedColumns: string[] = ['id', 'name', 'year', 'month', 'day', 'hour', 'workplace', 'role'];
  dataSource: MatTableDataSource<Audio>;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  getAudio(): void {
    this.recordsService.getRecords()
      .subscribe(records => {
        records.map(x => {
          const date = new Date(Date.parse(x.date + 'Z'));
          console.log(x.role)
          x.role = (x.role in [0, 1] ? (x.role.toString() === '0' ? 'Оператор' : 'Клиент') : 'Не указано');
          x.year = date.getFullYear();
          x.month = date.getMonth();
          x.day = date.getDay();
          x.hour = date.getHours();
          x.minute = date.getMinutes();
          x.ms = date.getMilliseconds();
        });
        this.records.next(records);
        this.dataSource = new MatTableDataSource<Audio>(this.records.value);
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
      });
  }


  constructor(
    public dialog: MatDialog,
    private audioService: AudioplayerService,
    private recordsService: AudioService,
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
    this.getAudio();
  }

  play(id: string, index: number) {
    console.log(id);
    const dialogRef = this.dialog.open(PlayerComponent);
    dialogRef.componentInstance.files = this.records.value;
    dialogRef.componentInstance.openFile(id, index);
    dialogRef.afterClosed().subscribe(result => {
      dialogRef.componentInstance.stop();
      console.log(`Dialog result: ${result}`);
    });
  }
}
