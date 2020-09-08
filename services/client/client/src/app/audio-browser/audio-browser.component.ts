import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {Audio} from '../interfaces/audio';
import {MatDialog} from '@angular/material/dialog';
import {MatSort} from '@angular/material/sort';
import {PlayerComponent} from '../player/player.component';
import { AudioplayerService } from '../services/audioplayer.service';
import { AudioService } from '../services/audio.service';
import {MatTableDataSource} from '@angular/material/table';
import {MatPaginator} from '@angular/material/paginator';
import {BehaviorSubject} from 'rxjs';
import {map} from 'rxjs/operators';
// import {MatPaginator} from '@angular/material/paginator';

@Component({
  selector: 'app-audio-browser',
  templateUrl: './audio-browser.component.html',
  styleUrls: ['./audio-browser.component.scss']
})
export class AudioBrowserComponent implements OnInit, AfterViewInit {
  // records: Audio[];
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
