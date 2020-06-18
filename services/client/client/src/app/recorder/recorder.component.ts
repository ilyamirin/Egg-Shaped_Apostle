import { Component, OnInit } from '@angular/core';
import {AudioService} from '../services/audio.service';
import {Microphone} from '../interfaces/microphone';

@Component({
  selector: 'app-recorder',
  templateUrl: './recorder.component.html',
  styleUrls: ['./recorder.component.scss']
})
export class RecorderComponent implements OnInit {

  constructor(
    private audioService: AudioService
  ) { }
  state = {
    error: false,
    playing: true,
    busy: false,

  };
  timeValue: 10;
  recordName: string;
  mic: Microphone;
  record(mic): void {
    this.audioService.record(mic.raspberry, mic.card, mic.name, this.timeValue)
      .subscribe(record => this.recordName = record);
  }

  ngOnInit(): void {
  }

}
