/* eslint no-new: 0, no-continue: 0 */
const $ = require('jquery');
const Chart = require('chart.js');

const options = {
  animation: false,
  legend: { display: false },
  tooltips: { bodyFontSize: 20 },
};

function draw_drop_points_by_state(_data) {
  const d = [];
  const l = [];
  const c = [];

  for (const state in labels) {
    if (typeof _data[state] !== 'number' || _data[state] === 0) {
      continue;
    }
    d.push(_data[state]);
    c.push(labels[state][2]);
    l.push($(labels[state][1]).text());
  }
  new Chart($('#overall_drop_points_by_state'), {
    type: 'doughnut',
    data: {
      labels: l,
      datasets: [
        {
          data: d,
          backgroundColor: c,
          hoverBackgroundColor: c,
        },
      ],
    },
    options,
  });
}

function draw_reports_by_state(_data) {
  const d = [];
  const l = [];
  const c = [];

  for (const state in labels) {
    if (typeof _data[state] !== 'number' || _data[state] === 0) {
      continue;
    }
    d.push(_data[state]);
    c.push(labels[state][2]);
    l.push($(labels[state][1]).text());
  }
  new Chart($('#reports_by_state'), {
    type: 'doughnut',
    data: {
      labels: l,
      datasets: [
        {
          data: d,
          backgroundColor: c,
          hoverBackgroundColor: c,
        },
      ],
    },
    options,
  });
}

$.get({
  url: '/numbers.json',
  success: data => {
    draw_drop_points_by_state(data.dropPoints);
    draw_reports_by_state(data.reports);
  },
});
