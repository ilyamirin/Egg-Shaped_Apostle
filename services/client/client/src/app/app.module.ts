import {NgModule} from '@angular/core';
import {AppComponent} from './app.component';
import {AnalyticsModule} from './analytics/analytics.module';
import {AudioBrowserModule} from './audio-browser/audio-browser.module';
import {DevicesModule} from './devices/devices.module';
import {FullTextSearchModule} from './full-text-search/full-text-search.module';
import {ListenerModule} from './listener/listener.module';
import {NavigationModule} from './navigation/navigation.module';
import {PlayerModule} from './player/player.module';
import {RecorderModule} from './recorder/recorder.module';
import {BrowserModule} from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {AppRoutingModule} from './app-routing.module';
import {HttpClientModule} from '@angular/common/http';
import {MatGridListModule} from '@angular/material/grid-list';


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    AppRoutingModule,
    BrowserAnimationsModule,
    BrowserModule,
    HttpClientModule,

    AnalyticsModule,
    AudioBrowserModule,
    DevicesModule,
    FullTextSearchModule,
    ListenerModule,
    NavigationModule,
    PlayerModule,
    RecorderModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
