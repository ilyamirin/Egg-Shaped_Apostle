import {Component, OnInit} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';

import {AudioService} from '../services/audio.service';
import {Microphone} from '../interfaces/microphone';
import {ListenerComponent} from '../listener/listener.component';
import {RecorderComponent} from '../recorder/recorder.component';
import {Location} from '@angular/common';


@Component({
  selector: 'app-devices',
  templateUrl: './devices.component.html',
  styleUrls: ['./devices.component.scss']
})
export class DevicesComponent implements OnInit {
  constructor(
    private audioService: AudioService,
    public dialog: MatDialog,
    private location: Location
  ) {
  }

  microphones: Microphone[];
  getAudio(): void {
    this.audioService.getMicrophones()
      .subscribe(microphones => this.microphones = microphones);
  }


  listen(mic: Microphone) {
    console.log(mic);
    const dialogRef = this.dialog.open(ListenerComponent);
    dialogRef.componentInstance.openStream(mic);
    dialogRef.afterClosed().subscribe(result => {
      dialogRef.componentInstance.stop();
      console.log(`Dialog result: ${result}`);
    });
  }

  record(mic: Microphone) {
    console.log(mic);
    const dialogRef = this.dialog.open(RecorderComponent);
    dialogRef.componentInstance.mic = mic;
    // dialogRef.componentInstance.openFile(id, index);
    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }

  update() {
    this.audioService.updateMicrophones();
    location.reload();
  }

  ngOnInit(): void {
    this.getAudio();
  }

}
