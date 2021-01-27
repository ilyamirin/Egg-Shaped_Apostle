import {NgModule} from '@angular/core';
import {DevicesComponent} from './devices.component';
import {MatIconModule} from '@angular/material/icon';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatCardModule} from '@angular/material/card';
import {FlexLayoutModule} from '@angular/flex-layout';
import {MatButtonModule} from '@angular/material/button';
import {MatTooltipModule} from '@angular/material/tooltip';
import {CommonModule} from '@angular/common';
import {MicrophoneCardModule} from '../microphone-card/microphone-card.module';


@NgModule({
  declarations: [
    DevicesComponent
  ],
  imports: [
    MatIconModule,
    MatGridListModule,
    MatCardModule,
    FlexLayoutModule,
    MatButtonModule,
    MatTooltipModule,
    CommonModule,

    MicrophoneCardModule
  ],
  exports: [
    DevicesComponent
  ]
})
export class DevicesModule {
}
