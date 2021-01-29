import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {DevicesComponent} from './devices/devices.component';


const routes: Routes = [
  // {path: 'audio', component: AudioBrowserComponent},
  // {path: 'nav', component: NavigationComponent},
  // {path: 'analytics', component: AnalyticsComponent},
  // {path: 'fts', component: FullTextSearchComponent},
  {path: 'devices', component: DevicesComponent},
  // { path: '', redirectTo: '/nav', pathMatch: 'full'}
  {path: '**', redirectTo: '/'}
];


@NgModule({
  imports: [
    RouterModule.forRoot(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule {
}
