import {NgModule} from '@angular/core';
import {AudioBrowserComponent} from './audio-browser.component';
import {MatTableModule} from '@angular/material/table';
import {MatSortModule} from '@angular/material/sort';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatPaginatorModule} from '@angular/material/paginator';


@NgModule({
  declarations: [
    AudioBrowserComponent
  ],
  imports: [
    MatTableModule,
    MatSortModule,
    MatFormFieldModule,
    MatInputModule,
    MatPaginatorModule
  ],
  exports: [
    AudioBrowserComponent
  ]
})
export class AudioBrowserModule {
}
