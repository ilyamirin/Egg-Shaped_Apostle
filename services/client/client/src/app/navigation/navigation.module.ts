import {NgModule} from '@angular/core';
import {NavigationComponent} from './navigation.component';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon';
import {CommonModule} from '@angular/common';
import {MatButtonModule} from '@angular/material/button';
import {MatListModule} from '@angular/material/list';
import {RouterModule} from '@angular/router';
import {ThemePickerModule} from '../theme-picker/theme-picker.module';


@NgModule({
  declarations: [
    NavigationComponent
  ],
  imports: [
    CommonModule,
    MatButtonModule,
    MatSidenavModule,
    MatToolbarModule,
    MatIconModule,
    MatListModule,
    RouterModule,
    ThemePickerModule
  ],
  exports: [
    NavigationComponent
  ]
})
export class NavigationModule {
}
