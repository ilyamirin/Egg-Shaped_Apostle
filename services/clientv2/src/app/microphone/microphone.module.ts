import {NgModule} from '@angular/core';
import {MicrophoneComponent} from './microphone.component';
import {MatCardModule} from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatTooltipModule} from '@angular/material/tooltip';
import {FlexLayoutModule} from '@angular/flex-layout';


@NgModule({
  declarations: [
    MicrophoneComponent
  ],
  imports: [
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    MatTooltipModule,

    FlexLayoutModule
  ],
  exports: [
    MicrophoneComponent
  ]
})
export class MicrophoneModule {
}
