import {NgModule} from '@angular/core';
import {AnalyticsComponent} from './analytics.component';
import {MatCardModule} from '@angular/material/card';
import {MatFormFieldModule} from '@angular/material/form-field';
import {FlexLayoutModule} from '@angular/flex-layout';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatInputModule} from '@angular/material/input';
import {MatRadioModule} from '@angular/material/radio';
import {ReactiveFormsModule} from '@angular/forms';
import {MatSelectModule} from '@angular/material/select';
import {MatIconModule} from '@angular/material/icon';
import {MatGridListModule} from '@angular/material/grid-list';
import {CommonModule} from '@angular/common';
import {MatButtonModule} from '@angular/material/button';
import {MatNativeDateModule} from '@angular/material/core';


@NgModule({
  declarations: [
    AnalyticsComponent
  ],
  imports: [
    MatCardModule,
    MatFormFieldModule,
    FlexLayoutModule,
    MatDatepickerModule,
    MatInputModule,
    MatRadioModule,
    ReactiveFormsModule,
    MatSelectModule,
    MatIconModule,
    MatGridListModule,
    CommonModule,
    MatButtonModule,
    MatNativeDateModule
  ],
  exports: [
    AnalyticsComponent
  ]
})
export class AnalyticsModule {
}
