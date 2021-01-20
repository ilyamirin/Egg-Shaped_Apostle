import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {AudioplayerService} from '../services/audioplayer.service';
import {AudioService} from '../services/audio.service';
import {StreamState} from '../interfaces/stream-state';


@Component({
  selector: 'app-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.scss']
})

export class PlayerComponent {
  constructor(
    public audioService: AudioplayerService,
    // public recordsService: AudioService,
  ) {
    /*recordsService.getRecords().subscribe(files => {
      this.files = files;
    });*/

    this.audioService.getState().subscribe(state => {
      this.state = state;
    });

  }

  public files: Array<any> = [];
  state: StreamState;
  currentFile: any = {};

  playStream(url) {
    this.audioService.playStream(url).subscribe(events => {
    });
  }

  openFile(file, index) {
    this.currentFile = {index, file};
    this.audioService.stop();
    this.playStream(file.url);
  }

  pause() {
    this.audioService.pause();
  }

  play() {
    this.audioService.play();
  }

  stop() {
    this.audioService.stop();
  }

  next() {
    const index = this.currentFile.index + 1;
    const file = this.files[index];
    this.openFile(file, index);
  }

  previous() {
    const index = this.currentFile.index - 1;
    const file = this.files[index];
    this.openFile(file, index);
  }

  isFirstPlaying() {
    return this.currentFile.index === 0;
  }

  isLastPlaying() {
    return this.currentFile.index === this.files.length - 1;
  }

  onSliderChangeEnd(change) {
    this.audioService.seekTo(change.value);
  }

}
