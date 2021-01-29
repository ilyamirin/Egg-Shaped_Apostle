import {NgModule} from '@angular/core';
import {NavigationComponent} from './navigation.component';
import {ToolbarModule} from '../toolbar/toolbar.module';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatCardModule} from '@angular/material/card';
import {MatListModule} from '@angular/material/list';
import {MatToolbarModule} from '@angular/material/toolbar';
import {RouterModule} from '@angular/router';
import {MatIconModule} from '@angular/material/icon';
import {CommonModule} from '@angular/common';


@NgModule({
  declarations: [
    NavigationComponent
  ],
  imports: [
    CommonModule,
    RouterModule,

    MatSidenavModule,
    MatListModule,
    MatToolbarModule,
    MatIconModule,

    ToolbarModule
  ],
  exports: [
    NavigationComponent
  ]
})
export class NavigationModule {
}
