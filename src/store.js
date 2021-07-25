const listeners = new Set();

const storeHandler = {
  get(target, key) {
    const value = target[key];
    return typeof value === 'object' ? new Proxy(value, storeHandler) : value;
  },
  set(target, key, value) {
    target[key] = value;
    notify();
    return true;
  }
}

const store = new Proxy({
  currentView: 'settings',
  groupSize: 2,
  neededAssignments: 1,
  currentAssignment: 0,
  participants: [],
  assignments: [
    [
      [
        { name: "Cartman"},
        { name: "Kyle"},
        { name: "Kenny"},
        { name: "Butters"}
      ],
      [
        { name: "Lisa"},
        { name: "Bart"},
        { name: "Homer"},
        { name: "Marge"}
      ],
      [
        { name: "Donald"},
        { name: "Mickey"},
        { name: "Goofy"},
        { name: "Pluto"}
      ]
    ],
    [
      [
        { name: "Cartman"},
        { name: "Bart"},
        { name: "Butters"},
        { name: "Goofy"},
      ],
      [
        { name: "Kyle"},
        { name: "Lisa"},
        { name: "Homer"},
        { name: "Marge"}
      ],
      [
        { name: "Kenny"},
        { name: "Donald"},
        { name: "Mickey"},
        { name: "Pluto"}
      ]
    ]
  ],
}, storeHandler);

function notify() {
  listeners.forEach(listener => listener(store))
}

export function addChangeListener(listener) {
  listeners.add(listener);
}

export default store;