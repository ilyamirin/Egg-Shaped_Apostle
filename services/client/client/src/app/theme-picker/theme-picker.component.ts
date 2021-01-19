import {ChangeDetectionStrategy, Component, OnInit, ViewEncapsulation} from '@angular/core';
import {Theme, ThemeStorage} from './theme-storage/theme-storage';
import {LiveAnnouncer} from '@angular/cdk/a11y';
import {MatIconRegistry} from '@angular/material/icon';
import {DomSanitizer} from '@angular/platform-browser';
import {StyleManager} from '../style-manager';


@Component({
  selector: 'app-theme-picker',
  templateUrl: './theme-picker.component.html',
  styleUrls: ['./theme-picker.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  encapsulation: ViewEncapsulation.None
})
export class ThemePickerComponent implements OnInit {

  currentTheme: Theme;

  // The below colors need to align with the themes defined in theme-picker.scss
  themes: Theme[] = [
    {
      primary: '#00BCD4',
      accent: '#FFC107',
      displayName: 'Cyan & Amber',
      name: 'cyan-amber',
      isDark: false,
      isDefault: true
    },
    {
      primary: '#9C27B0',
      accent: '#4CAF50',
      displayName: 'Purple & Green',
      name: 'purple-green',
      isDark: true
    }
  ];

  constructor(public styleManager: StyleManager,
              private _themeStorage: ThemeStorage,
              private liveAnnouncer: LiveAnnouncer,
              iconRegistry: MatIconRegistry,
              sanitizer: DomSanitizer) {
    iconRegistry.addSvgIcon('theme-preview',
      sanitizer.bypassSecurityTrustResourceUrl(
        'assets/img/icons/theme-preview-icon.svg'));
    const themeName = this._themeStorage.getStoredThemeName();

    if (themeName) {
      this.selectTheme(themeName);
    }
  }

  ngOnInit() {
    this.selectTheme('cyan-amber');
  }

  selectTheme(themeName: string) {
    const theme = this.themes.find(currentTheme => currentTheme.name === themeName);

    if (!theme) {
      return;
    }

    this.currentTheme = theme;

    if (theme.isDefault) {
      this.styleManager.removeStyle('theme');
    } else {
      this.styleManager.setStyle('theme', `assets/${theme.name}.css`);
    }

    if (this.currentTheme) {
      this.liveAnnouncer.announce(`${theme.displayName} theme selected.`, 'polite', 3000);
      this._themeStorage.storeTheme(this.currentTheme);
    }
  }

}
