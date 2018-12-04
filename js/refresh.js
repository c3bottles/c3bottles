const $ = require('jquery');
const list = require('./list');
const map = require('./map');

const apiUrl = $('meta[name="endpoint"]').data('api');

function refreshDropPoint(num) {
  if (map.isInitialized()) {
    map.drawMarker(num);
  }
  if (list.isInitialized()) {
    list.drawRow(num);
  }
}

module.exports.refreshDropPoint = refreshDropPoint;

function update(ts) {
  const _ts = Date.now() / 1000;

  $.ajax({
    type: 'POST',
    url: apiUrl,
    data: {
      action: 'dp_json',
      ts,
    },
    dataType: 'json',
    success(response) {
      $.extend(true, drop_points, response);
      for (const num in response) {
        refreshDropPoint(num);
      }
    },
    complete() {
      setTimeout(() => {
        update(_ts);
      }, 120000);
    },
  });
}

module.exports.startPeriodicRefresh = function() {
  const ts = Date.now() / 1000;

  setTimeout(() => {
    update(ts);
  }, 120000);
};
