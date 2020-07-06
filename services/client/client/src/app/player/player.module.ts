import {NgModule} from '@angular/core';
import {PlayerComponent} from './player.component';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon';
import {MatListModule} from '@angular/material/list';
import {MatSliderModule} from '@angular/material/slider';
import {MatButtonModule} from '@angular/material/button';
import {CommonModule} from '@angular/common';


@NgModule({
  declarations: [
    PlayerComponent
  ],
  imports: [
    MatToolbarModule,
    MatIconModule,
    MatListModule,
    MatSliderModule,
    MatButtonModule,
    CommonModule
  ],
  exports: [
    PlayerComponent
  ]
})
export class PlayerModule {
}
