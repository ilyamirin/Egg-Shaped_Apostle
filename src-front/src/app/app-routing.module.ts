import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { PlaceInfoComponent } from './place-info/place-info.component';

const routes: Routes = [{
  path: '',
  component: AppComponent,
  children: [
    {
      path: '',
      component: HomeComponent
    },
    {
      path: 'place/:id',
      component: PlaceInfoComponent
    }
  ]
}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
