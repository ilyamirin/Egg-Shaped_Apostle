import {NgModule} from '@angular/core';
import {AudioBrowserComponent} from './audio-browser.component';
import {MatTableModule} from '@angular/material/table';


@NgModule({
  declarations: [
    AudioBrowserComponent
  ],
  imports: [
    MatTableModule
  ],
  exports: [
    AudioBrowserComponent
  ]
})
export class AudioBrowserModule {
}
