import {NgModule} from '@angular/core';
import {RecorderComponent} from './recorder.component';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatSliderModule} from '@angular/material/slider';
import {FormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {MatInputModule} from '@angular/material/input';


@NgModule({
  declarations: [
    RecorderComponent
  ],
  imports: [
    MatToolbarModule,
    MatIconModule,
    MatFormFieldModule,
    MatSliderModule,
    FormsModule,
    MatButtonModule,
    MatInputModule
  ],
  exports: [
    RecorderComponent
  ]
})
export class RecorderModule {
}
