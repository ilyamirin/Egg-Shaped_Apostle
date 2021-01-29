import {Component, Input, OnInit} from '@angular/core';
import {Microphone} from '../model';


@Component({
  selector: 'app-microphone',
  templateUrl: './microphone.component.html',
  styleUrls: ['./microphone.component.scss']
})
export class MicrophoneComponent implements OnInit {

  @Input()
  microphone: Microphone;

  constructor() {
  }

  ngOnInit(): void {
  }

}
