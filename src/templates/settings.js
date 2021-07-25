import { html } from 'lit-html';

import store from '../store';

import settingsParticipants from  './settings-participants';
import settingsParameters from './settings-parameters';

export default () => html`
<div class="container py-5">
  <h2 class="mb-4 page-title">Einstellungen</h2>

  ${settingsParameters()}

  <hr class="my-4" />

  ${settingsParticipants()}

  <button 
    type="button" 
    class="btn btn-lg btn-outline-primary w-100 mt-5"
    @click="${() => store.currentView = 'assignments'}"
  >
    Teilnehmer Mixen
  </button>
</div>
`;