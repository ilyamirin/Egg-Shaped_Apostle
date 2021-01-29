import {Component, OnInit, ViewChild} from '@angular/core';
import {MatSidenav} from '@angular/material/sidenav';
import {SidenavService} from '../service/sidenav.service';
import {NavRoute} from '../model/nav-route.model';


@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit {

  @ViewChild('commandbarSidenav', {static: true})
  public sidenav: MatSidenav;

  navRoutes: NavRoute[];

  constructor(
    private commandBarSidenavService: SidenavService
  ) {
  }

  ngOnInit(): void {
    this.navRoutes = [
      {
        icon: 'mic',
        title: 'Микрофоны',
        route: '/devices'
      },
      {
        icon: 'album',
        title: 'Записи',
        route: '/audio'
      },
      {
        icon: 'bar_chart',
        title: 'Аналитика',
        route: '/analytics'
      },
      {
        icon: 'search',
        title: 'Поиск',
        route: '/fts'
      }
    ];

    this.commandBarSidenavService.setSidenav(this.sidenav);
  }

}
