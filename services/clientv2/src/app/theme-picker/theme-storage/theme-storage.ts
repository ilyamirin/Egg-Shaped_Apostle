import {EventEmitter, Injectable} from '@angular/core';
import {Theme} from '../../model';


@Injectable()
export class ThemeStorage {

  static storageKey = 'theme-storage-current-name';

  onThemeUpdate: EventEmitter<Theme> = new EventEmitter<Theme>();

  storeTheme(theme: Theme) {
    try {
      window.localStorage[ThemeStorage.storageKey] = theme.name;
    } catch {
    }

    this.onThemeUpdate.emit(theme);
  }

  getStoredThemeName(): string | null {
    try {
      return window.localStorage[ThemeStorage.storageKey] || null;
    } catch {
      return null;
    }
  }

  clearStorage() {
    try {
      window.localStorage.removeItem(ThemeStorage.storageKey);
    } catch {
    }
  }

}
