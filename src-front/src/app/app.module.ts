import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {FormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';

import {HomeComponent} from './home/home.component';
import {PlaceCardComponent} from '../component/place-card/place-card.component';
import {PlaceInfoComponent} from './place-info/place-info.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {
  NbButtonModule,
  NbCalendarModule,
  NbCardModule,
  NbDatepickerModule,
  NbInputModule,
  NbLayoutModule,
  NbSelectModule,
  NbThemeModule
} from '@nebular/theme';
import {NbEvaIconsModule} from '@nebular/eva-icons';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    PlaceCardComponent,
    PlaceInfoComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,

    /*Nebular modules*/
    NbThemeModule.forRoot({name: 'default'}),
    NbLayoutModule,
    NbEvaIconsModule,
    NbCardModule,
    NbInputModule,
    NbDatepickerModule.forRoot(),
    NbDatepickerModule,
    NbCalendarModule,
    NbButtonModule,
    NbSelectModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
