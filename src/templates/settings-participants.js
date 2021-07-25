import { html } from 'lit-html';

import store from '../store';

function add(e) {
  if(e.key !== 'Enter') return;

  store.participants.push(e.target.value);
  e.target.value = '';
}

function clearAll() {
  store.participants = [];
}

function clear(idx) {
  store.participants.splice(idx, 1);
}

export default () => html`
  <div class="row align-items-center mb-4">
    <div class="col">
      <h4 class="m-0">Teilnehmer</h4>
    </div>

    <div class="col-auto">
      <input
        @keydown="${add}"
        class="form-control"
        type="text"
        placeholder="Teilnehmer hinzufügen"
      />
    </div>
  </div>

  <div class="list-group mb-4 shadow">
    ${ store.participants.map((participant, idx) => html`
      <div class="list-group-item">
        <div class="row align-items-center">
          <div class="col">
            <strong>${participant}</strong>
          </div>

          <div class="col-auto">
            <button
              type="button"
              class="btn-close p-2"
              @click=${() => clear(idx)}></button>
          </div>
        </div>
      </div>
    `)}
  </div>

  <button
    type="button"
    class="btn btn-danger"
    @click="${clearAll}">Alle löschen</button>
`;