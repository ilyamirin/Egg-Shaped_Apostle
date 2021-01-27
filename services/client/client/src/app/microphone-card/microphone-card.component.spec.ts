import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MicrophoneCardComponent } from './microphone-card.component';

describe('MicrophoneCardComponent', () => {
  let component: MicrophoneCardComponent;
  let fixture: ComponentFixture<MicrophoneCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MicrophoneCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MicrophoneCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
