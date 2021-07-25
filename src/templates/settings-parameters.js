import { html } from 'lit-html';
import { live } from 'lit-html/directives/live'

import store from '../store';

export default () => html`
  <h4 class="mb-4">Parameter</h4>

  <div class="list-group shadow mb-5">
    <div class="list-group-item">
      <div class="row align-items-center">
        <div class="col-9 col-md-10">
          <strong>Gruppengröße</strong>
          <p class="mb-2">Wie viele Personen fasst eine Gruppe?</p>
        </div>

        <div class="col-3 col-md-2">
          <input 
            class="form-control" 
            type="number" 
            min="2" 
            placeholder="2"
            .value="${live(store.groupSize)}"
            @input="${(e) => store.groupSize = parseInt(e.target.value, 10)}"
          >
        </div>
      </div>
    </div>

    <div class="list-group-item">
      <div class="row align-items-center">
        <div class="col-9 col-md-10">
          <strong>Anzahl Gruppenarbeiten</strong>
          <p class="mb-2">Wie oft müssen verschiedene Gruppen gebildet werden?</p>
        </div>

        <div class="col-3 col-md-2">
          <input 
            class="form-control" 
            type="number" 
            min="1" 
            placeholder="1"
            .value="${store.neededAssignments}"
            @input="${(e) => store.neededAssignments = parseInt(e.target.value, 10)}">
        </div>
      </div>
    </div>
  </div>
`;