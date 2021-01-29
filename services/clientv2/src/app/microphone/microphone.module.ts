import {NgModule} from '@angular/core';
import {MicrophoneComponent} from './microphone.component';
import {MatCardModule} from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';


@NgModule({
  declarations: [
    MicrophoneComponent
  ],
  imports: [
    MatButtonModule,
    MatCardModule,
    MatIconModule
  ],
  exports: [
    MicrophoneComponent
  ]
})
export class MicrophoneModule {
}
