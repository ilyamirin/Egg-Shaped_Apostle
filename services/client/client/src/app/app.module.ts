import {NgModule} from '@angular/core';
import {AppComponent} from './app.component';
import {CommonModule} from '@angular/common';
import {AnalyticsModule} from './analytics/analytics.module';
import {AudioBrowserModule} from './audio-browser/audio-browser.module';
import {DevicesModule} from './devices/devices.module';
import {FullTextSearchModule} from './full-text-search/full-text-search.module';
import {ListenerModule} from './listener/listener.module';
import {NavigationModule} from './navigation/navigation.module';
import {PlayerModule} from './player/player.module';
import {RecorderModule} from './recorder/recorder.module';
import {ThemePickerModule} from './theme-picker/theme-picker.module';
import {BrowserModule} from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {AppRoutingModule} from './app-routing.module';
import {HttpClientModule} from '@angular/common/http';


@NgModule({
  declarations: [AppComponent],
  imports: [
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    BrowserModule,

    AnalyticsModule,
    AudioBrowserModule,
    DevicesModule,
    FullTextSearchModule,
    ListenerModule,
    NavigationModule,
    PlayerModule,
    RecorderModule,
    ThemePickerModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
