import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {NavigationModule} from './navigation/navigation.module';
import {ToolbarModule} from './toolbar/toolbar.module';
import {AppRoutingModule} from './app-routing.module';
import {DeviceModule} from './devices/device.module';


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    // Angular modules
    BrowserModule,
    BrowserAnimationsModule,

    // Self modules
    ToolbarModule,
    NavigationModule,
    DeviceModule,

    AppRoutingModule
  ],
  providers: [],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule {
}
