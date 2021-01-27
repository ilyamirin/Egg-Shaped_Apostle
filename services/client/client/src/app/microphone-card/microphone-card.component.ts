import {Component, Input, OnInit} from '@angular/core';
import {Microphone} from '../interfaces/microphone';
import {ListenerComponent} from '../listener/listener.component';
import {MatDialog} from '@angular/material/dialog';


@Component({
  selector: 'app-microphone-card',
  templateUrl: './microphone-card.component.html',
  styleUrls: ['./microphone-card.component.scss']
})
export class MicrophoneCardComponent implements OnInit {

  @Input()
  microphone: Microphone;

  constructor(
    public dialog: MatDialog
  ) {
  }

  ngOnInit(): void {
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

}
