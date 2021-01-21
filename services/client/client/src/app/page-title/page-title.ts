import {Injectable} from '@angular/core';
import {Title} from '@angular/platform-browser';


@Injectable({
  providedIn: 'root'
})
export class PageTitle {

  _title = '';
  _originalTitle = 'SberEye';

  get title(): string {
    return this._title;
  }

  set title(title: string) {
    this._title = title;

    if (title !== '') {
      title = `${title} | ${this._originalTitle}`;
    } else {
      title = this._originalTitle;
    }

    this.bodyTitle.setTitle(title);
  }

  constructor(private bodyTitle: Title) {
  }

}
