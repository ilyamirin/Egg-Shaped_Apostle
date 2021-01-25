import {NgModule} from '@angular/core';
import {AnalysisDialogueComponent} from './analysis-dialogue.component';
import {MatGridListModule} from '@angular/material/grid-list';


@NgModule({
  declarations: [
    AnalysisDialogueComponent
  ],
  imports: [
    MatGridListModule
  ],
  exports: [
    AnalysisDialogueComponent
  ],
  entryComponents: [
    AnalysisDialogueComponent
  ]
})
export class AnalysisDialogueModule {
}
