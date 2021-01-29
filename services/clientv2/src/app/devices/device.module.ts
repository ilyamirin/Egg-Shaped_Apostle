import {NgModule} from '@angular/core';
import {DevicesComponent} from './devices.component';
import {MicrophoneModule} from '../microphone/microphone.module';


@NgModule({
  declarations: [
    DevicesComponent
  ],
  imports: [
    MicrophoneModule
  ],
  exports: [
    DevicesComponent
  ]
})
export class DeviceModule {
}
