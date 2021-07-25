import { html } from 'lit-html';

import store from '../store';

function getGroups() {
  return store.assignments[store.currentAssignment];
}

function prev() {
  store.currentAssignment = Math.max(0, store.currentAssignment - 1);
}

function next() {
  store.currentAssignment = Math.min(store.currentAssignment + 1, store.assignments.length - 1);
}

export default () => html`
<div class="v-assignments container py-5 text-center">
  <h1 class="mb-5 page-title row align-items-center justify-content-center">
    <span class="v-assignments__prev" @click="${prev}"></span> 
    <span class="v-assignments__title">Aufteilung ${store.currentAssignment + 1}</span>
    <span class="v-assignments__next" @click="${next}"></span> 
  </h1>

  <div class="grid my-5">
    ${getGroups()?.map((group, idx) => html`
      <div class="card">
        <h5 class="card-header">Gruppe ${idx + 1}</h5>

        <ul class="list-group list-group-flush">
          ${group.map(participant => html`
            <li class="list-group-item">${participant.name}</li>
          `)}
        </ul>
      </div>
    `)}
  </div>

  <button 
    type="button" 
    class="btn btn-lg btn-outline-primary w-100 mt-5"
    @click="${() => store.currentView = 'settings'}"
  >
    Einstellungen
  </button>
</div>
`;