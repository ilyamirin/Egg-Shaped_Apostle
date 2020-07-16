import {NgModule} from '@angular/core';
import {FullTextSearchComponent} from './full-text-search.component';
import {FlexLayoutModule} from '@angular/flex-layout';
import {MatCardModule} from '@angular/material/card';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatRadioModule} from '@angular/material/radio';
import {MatSelectModule} from '@angular/material/select';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {CommonModule} from '@angular/common';
import {MatTooltipModule} from '@angular/material/tooltip';
import {MatNativeDateModule} from '@angular/material/core';


@NgModule({
  declarations: [
    FullTextSearchComponent
  ],
  imports: [
    FlexLayoutModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatDatepickerModule,
    FormsModule,
    MatRadioModule,
    MatSelectModule,
    ReactiveFormsModule,
    MatIconModule,
    MatButtonModule,
    CommonModule,
    MatTooltipModule,
    MatNativeDateModule
  ],
  exports: [
    FullTextSearchComponent
  ]
})
export class FullTextSearchModule {
}
