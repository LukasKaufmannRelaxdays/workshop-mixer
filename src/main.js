import * as mixer from "../__target__/main.js";
window.mixer = mixer;
var header = document.createElement("h1");
header.innerHTML = "Workshop Mixer";
document.body.appendChild(header);

header.style.textAlign = "center";
header.style.margin = "0";
header.style.padding = "0";
header.style.fontSize = "2em";
header.style.fontFamily = "sans-serif";

document.body.style.backgroundColor = "#f0f0f0";

document.body.style.padding = "1em";
document.body.style.border = "1px solid #ccc";
document.body.style.borderRadius = "5px";
document.body.style.boxShadow = "0 0 5px #ccc";

var input = document.createElement("input");
input.type = "text";
input.style.width = "100%";
input.style.height = "2em";
input.style.fontSize = "1.5em";
input.style.fontFamily = "sans-serif";
input.style.padding = "0.5em";
input.style.border = "1px solid #ccc";
input.style.borderRadius = "5px";
input.style.boxShadow = "0 0 5px #ccc";
input.value =
  "Alice, Bob, Charlie, David, Eve, Fred, Grace, Harriet, Ileana, Joseph, Kincaid, Larry";
document.body.appendChild(input);

input.style.marginTop = "1em";

input.style.fontSize = "1em";

function countNames() {
  var names = input.value.split(",");
  return names.length;
}

var label = document.createElement("label");
label.innerHTML = "Number of participants: " + countNames();
document.body.appendChild(label);

setInterval(function () {
  label.innerHTML = "Number of participants: " + countNames();
}, 1000);

var plus = document.createElement("button");
plus.innerHTML = "+";
plus.style.fontSize = "1.5em";
plus.style.fontFamily = "sans-serif";
plus.style.padding = "0.5em";
plus.style.border = "1px solid #ccc";
plus.style.borderRadius = "5px";
plus.style.boxShadow = "0 0 5px #ccc";
plus.style.marginTop = "1em";
plus.style.marginLeft = "1em";
plus.style.marginRight = "1em";
plus.style.cursor = "pointer";
document.body.appendChild(plus);

plus.style.position = "absolute";
plus.style.bottom = "0";
plus.style.left = "50%";
plus.style.marginLeft = "-0.5em";

plus.style.backgroundColor = "#ccc";

function getLastInput() {
  var inputs = document.getElementsByTagName("input");
  return inputs[inputs.length - 1];
}

var inputs = [];

function addParticipant(input) {
  input.style.width = "100%";
  input.style.height = "2em";
  input.style.fontSize = "1.5em";
  input.style.fontFamily = "sans-serif";
  input.style.padding = "0.5em";
  input.style.border = "1px solid #ccc";
  input.style.borderRadius = "5px";
  input.style.boxShadow = "0 0 5px #ccc";
}

plus.onclick = function () {
  var input = document.createElement("input");
  addParticipant(input);
  input.style.marginTop = "1em";
  input.style.fontSize = "1em";
  document.body.appendChild(input);
  inputs.push(input);
};

var warningDisplayed = false;

function displayWarning(input) {
  var warning = document.createElement("div");
  warning.innerHTML =
    'The number of "o" should match the number of participants';
  warning.style.color = "red";
  warning.style.fontSize = "0.8em";
  warning.style.fontFamily = "sans-serif";
  warning.style.padding = "0.5em";
  warning.style.border = "1px solid #ccc";
  warning.style.borderRadius = "5px";
  warning.style.boxShadow = "0 0 5px #ccc";
  warning.style.position = "absolute";
  warning.style.bottom = "0";
  warning.style.left = "50%";
  warning.style.marginLeft = "-0.5em";
  warning.style.cursor = "pointer";
  document.body.appendChild(warning);
  return warning;
}

var warning;

function checkO(input) {
  if (countO(input) !== countNames()) {
    if (!warningDisplayed) {
      warning = displayWarning(input);
      warningDisplayed = true;
    }
    warning.style.display = "block";
  } else {
    if (warningDisplayed) {
      warning.style.display = "none";
    }
    warningDisplayed = false;
  }
}

setInterval(function () {
  for (var i = 0; i < inputs.length; i++) {
    checkO(inputs[i]);
  }
}, 1000);

function countO(input) {
  return input.value.split("o").length - 1;
}

var submit = document.createElement("button");
submit.innerHTML = "Submit";
submit.style.fontSize = "1.5em";
submit.style.fontFamily = "sans-serif";
submit.style.padding = "0.5em";
submit.style.border = "1px solid #ccc";
submit.style.borderRadius = "5px";
submit.style.boxShadow = "0 0 5px #ccc";
submit.style.position = "absolute";
submit.style.bottom = "0";
submit.style.right = "0";
submit.style.marginRight = "1em";
submit.style.cursor = "pointer";
document.body.appendChild(submit);

submit.style.backgroundColor = "#ccc";

function getStrings() {
  var strings = [];
  for (var i = 0; i < inputs.length; i++) {
    strings.push(inputs[i].value);
  }
  return strings;
}
var result;
submit.onclick = function () {
  result = mixer.improver(input.value.split(","), getStrings());

  var meetingMatrix = result.meetingMatrix;
  var table = document.createElement("table");
  document.body.appendChild(table);
  var tableBody = document.createElement("tbody");
  table.appendChild(tableBody);
  for (var i = 0; i < meetingMatrix.length; i++) {
    var row = document.createElement("tr");
    tableBody.appendChild(row);
    for (var j = 0; j < meetingMatrix[i].length; j++) {
      var cell = document.createElement("td");
      row.appendChild(cell);
      cell.innerHTML = meetingMatrix[i][j];
    }
  }
  table.style.border = "1px solid #ccc"

  var plan = result.plan;
  var table = document.createElement("table");
  document.body.appendChild(table);
  var tableBody = document.createElement("tbody");
  table.appendChild(tableBody);
  for (var i = 0; i < plan.length; i++) {
    var row = document.createElement("tr");
    tableBody.appendChild(row);
    for (var j = 0; j < plan[i].length; j++) {
      var cell = document.createElement("td");
      row.appendChild(cell);
      cell.innerHTML = "";
      cell.style.border =  "1px solid #ccc";
      for (var k = 0; k < plan[i][j].length; k++) {
        cell.innerHTML += plan[i][j][k] + "<br>";
      }
    }
  }
};
