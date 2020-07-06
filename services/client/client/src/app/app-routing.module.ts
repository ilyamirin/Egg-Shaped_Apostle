import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {AnalyticsComponent} from './analytics/analytics.component';
import {AudioBrowserComponent} from './audio-browser/audio-browser.component';
import {FullTextSearchComponent} from './full-text-search/full-text-search.component';
import {DevicesComponent} from './devices/devices.component';


const routes: Routes = [
  {path: 'audio', component: AudioBrowserComponent},
  // {path: 'nav', component: NavigationComponent},
  {path: 'analytics', component: AnalyticsComponent},
  {path: 'fts', component: FullTextSearchComponent},
  {path: 'devices', component: DevicesComponent},
  // { path: '', redirectTo: '/nav', pathMatch: 'full'}
  {path: '**', redirectTo: '/'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
