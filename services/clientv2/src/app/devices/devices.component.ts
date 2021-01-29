import { Component, OnInit } from '@angular/core';
import {Microphone} from '../model';

@Component({
  selector: 'app-devices',
  templateUrl: './devices.component.html',
  styleUrls: ['./devices.component.scss']
})
export class DevicesComponent implements OnInit {

  microphone: Microphone;

  constructor(
  ) {
  }

  ngOnInit(): void {
    this.microphone = {
      mic: 1,
      raspberry: 1,
      card: 1,
      workplace: '1',
      role: 'Оператор',
      status: 'good'
    };
  }

}
