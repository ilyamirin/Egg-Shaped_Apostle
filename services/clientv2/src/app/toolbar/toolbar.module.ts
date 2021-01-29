import {NgModule} from '@angular/core';
import {ToolbarComponent} from './toolbar.component';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatMenuModule} from '@angular/material/menu';
import {MatDividerModule} from '@angular/material/divider';
import {FlexLayoutModule} from '@angular/flex-layout';
import {MatTooltipModule} from '@angular/material/tooltip';
import {ThemePickerModule} from '../theme-picker/theme-picker.module';


@NgModule({
  declarations: [
    ToolbarComponent
  ],
  imports: [
    MatButtonModule,
    MatIconModule,
    MatToolbarModule,
    MatMenuModule,
    MatDividerModule,
    MatTooltipModule,

    FlexLayoutModule,

    ThemePickerModule
  ],
  exports: [
    ToolbarComponent
  ]
})
export class ToolbarModule {
}
