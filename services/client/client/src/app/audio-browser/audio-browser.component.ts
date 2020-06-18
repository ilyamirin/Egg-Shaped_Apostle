import {Component, OnInit} from '@angular/core';
import {Audio} from '../interfaces/audio';
import {MatDialog} from '@angular/material/dialog';
import {PlayerComponent} from '../player/player.component';
import { AudioplayerService } from '../services/audioplayer.service';
import { AudioService } from '../services/audio.service';

@Component({
  selector: 'app-audio-browser',
  templateUrl: './audio-browser.component.html',
  styleUrls: ['./audio-browser.component.scss']
})
export class AudioBrowserComponent implements OnInit {
  records: Audio[];
  displayedColumns: string[] = ['id', 'date', 'workplace', 'role'];

  getAudio(): void {
    this.recordsService.getRecords()
      .subscribe(records => this.records = records);
  }
  constructor(
    public dialog: MatDialog,
    private audioService: AudioplayerService,
    private recordsService: AudioService,
  ) {
  }

  ngOnInit(): void {
    this.getAudio();
  }

  play(id: string, index: number) {
    console.log(id);
    const dialogRef = this.dialog.open(PlayerComponent);
    dialogRef.componentInstance.files = this.records;
    dialogRef.componentInstance.openFile(id, index);
    dialogRef.afterClosed().subscribe(result => {
      dialogRef.componentInstance.stop();
      console.log(`Dialog result: ${result}`);
    });
  }

}
