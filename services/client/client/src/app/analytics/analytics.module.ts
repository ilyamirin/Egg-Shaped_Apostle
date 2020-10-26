import {NgModule} from '@angular/core';
import {AnalyticsComponent} from './analytics.component';
import {MatCardModule} from '@angular/material/card';
import {MatFormFieldModule} from '@angular/material/form-field';
import {FlexLayoutModule} from '@angular/flex-layout';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatInputModule} from '@angular/material/input';
import {MatRadioModule} from '@angular/material/radio';
import {MatSelectModule} from '@angular/material/select';
import {MatIconModule} from '@angular/material/icon';
import {MatGridListModule} from '@angular/material/grid-list';
import {CommonModule} from '@angular/common';
import {MatButtonModule} from '@angular/material/button';
import {MatNativeDateModule} from '@angular/material/core';
import {MatTableModule} from '@angular/material/table';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatTooltipModule} from '@angular/material/tooltip';



@NgModule({
  declarations: [
    AnalyticsComponent
  ],
    imports: [
        MatCardModule,
        MatFormFieldModule,
        FlexLayoutModule,
        FormsModule,
        MatDatepickerModule,
        MatInputModule,
        MatRadioModule,
        ReactiveFormsModule,
        MatSelectModule,
        MatIconModule,
        MatGridListModule,
        CommonModule,
        MatButtonModule,
        MatNativeDateModule,
        MatTableModule
    ],
  exports: [
    AnalyticsComponent
  ]
})
export class AnalyticsModule {
}
