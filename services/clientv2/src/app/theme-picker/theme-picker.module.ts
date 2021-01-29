import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {ThemePickerComponent} from './theme-picker.component';
import {MatMenuModule} from '@angular/material/menu';
import {ThemeStorage} from './theme-storage/theme-storage';
import {StyleManager} from '../style-manager';
import {HttpClientModule} from '@angular/common/http';


@NgModule({
  declarations: [
    ThemePickerComponent
  ],
  imports: [
    CommonModule,
    HttpClientModule,

    MatButtonModule,
    MatMenuModule,
    MatIconModule
  ],
  exports: [
    ThemePickerComponent
  ],
  providers: [
    StyleManager,
    ThemeStorage
  ]
})
export class ThemePickerModule {
}
