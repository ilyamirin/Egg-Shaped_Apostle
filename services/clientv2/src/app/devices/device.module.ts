import {NgModule} from '@angular/core';
import {DevicesComponent} from './devices.component';
import {MicrophoneModule} from '../microphone/microphone.module';
import {CommonModule} from '@angular/common';
import {FlexLayoutModule} from '@angular/flex-layout';


@NgModule({
  declarations: [
    DevicesComponent
  ],
  imports: [
    CommonModule,

    MicrophoneModule,

    FlexLayoutModule
  ],
  exports: [
    DevicesComponent
  ]
})
export class DeviceModule {
}
