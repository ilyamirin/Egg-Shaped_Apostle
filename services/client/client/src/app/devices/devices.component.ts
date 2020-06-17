import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-devices',
  templateUrl: './devices.component.html',
  styleUrls: ['./devices.component.scss']
})
export class DevicesComponent implements OnInit {
  devices: object[] = [
    {
      id: 1,
      raspberry: 1,
      card: 0,
      workplace: 1,
      role: 0
    },
    {
      id: 2,
      raspberry: 1,
      card: 1,
      workplace: 1,
      role: 1
    },
    {
      id: 3,
      raspberry: 1,
      card: 2,
      workplace: 2,
      role: 1
    },
    {
      id: 1,
      raspberry: 1,
      card: 0,
      workplace: 1,
      role: 0
    },
    {
      id: 2,
      raspberry: 1,
      card: 1,
      workplace: 1,
      role: 1
    },
    {
      id: 3,
      raspberry: 1,
      card: 2,
      workplace: 2,
      role: 1
    },
    {
      id: 1,
      raspberry: 1,
      card: 0,
      workplace: 1,
      role: 0
    },
    {
      id: 2,
      raspberry: 1,
      card: 1,
      workplace: 1,
      role: 1
    },
    {
      id: 3,
      raspberry: 1,
      card: 2,
      workplace: 2,
      role: 1
    },

  ];
  constructor() { }

  ngOnInit(): void {
  }

}
