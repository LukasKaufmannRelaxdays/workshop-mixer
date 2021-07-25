import { render } from 'lit-html';

import 'bootstrap/js/dist/offcanvas';

import store, { addChangeListener } from './store';
import settings from './templates/settings';
import assignments from './templates/assignments';

const views = { settings, assignments };

function updateUi() {
  render(views[store.currentView](), document.body);
}

addChangeListener(updateUi);
updateUi();