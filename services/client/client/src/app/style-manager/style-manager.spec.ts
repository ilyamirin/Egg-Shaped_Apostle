import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StyleManagerComponent } from './style-manager';

describe('StyleManagerComponent', () => {
  let component: StyleManagerComponent;
  let fixture: ComponentFixture<StyleManagerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StyleManagerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StyleManagerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
