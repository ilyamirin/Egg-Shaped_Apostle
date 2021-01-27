import {NgModule} from '@angular/core';
import {MicrophoneCardComponent} from './microphone-card.component';
import {MatCardModule} from '@angular/material/card';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {FlexLayoutModule} from '@angular/flex-layout';
import {CommonModule} from '@angular/common';


@NgModule({
  declarations: [
    MicrophoneCardComponent
  ],
  imports: [
    CommonModule,

    FlexLayoutModule,
    MatCardModule,
    MatIconModule,
    MatButtonModule
  ],
  exports: [
    MicrophoneCardComponent
  ]
})
export class MicrophoneCardModule {
}
