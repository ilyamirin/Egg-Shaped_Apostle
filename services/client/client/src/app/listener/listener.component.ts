import { Component, OnInit } from '@angular/core';
import { AudioplayerService } from '../services/audioplayer.service';
import {StreamState} from '../interfaces/stream-state';
import {Microphone} from '../interfaces/microphone';


@Component({
  selector: 'app-listener',
  templateUrl: './listener.component.html',
  styleUrls: ['./listener.component.scss']
})

export class ListenerComponent implements OnInit {
  constructor(
    private audioService: AudioplayerService,
    ) { }

  state = {
    playing: true,
    error: false
  };

  pause() {
    this.audioService.pause();
    this.state.playing = false;
  }

  playStream(url) {
    this.audioService.playStream(url).subscribe(events => {
    });
  }

  openStream(mic: Microphone) {
    this.audioService.stop();
    this.playStream('http://127.0.0.1:5722/microphone/19/stream');
  }

  play() {
    this.audioService.play();
    this.state.playing = true;
  }

  stop() {
    this.audioService.stop();
  }

  ngOnInit(): void {
  }

}
