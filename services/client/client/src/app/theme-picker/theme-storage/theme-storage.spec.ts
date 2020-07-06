import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ThemeStorageComponent } from './theme-storage';

describe('ThemeStorageComponent', () => {
  let component: ThemeStorageComponent;
  let fixture: ComponentFixture<ThemeStorageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ThemeStorageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ThemeStorageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
