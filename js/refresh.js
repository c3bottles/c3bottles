const $ = require('jquery');
const map = require('./map');

const api_url = $('meta[name="endpoint"]').data('api');

function refreshDropPoint(num) {
  if (map.isInitialized()) {
    map.drawMarker(num);
  }
  if (typeof dt != 'undefined') {
    draw_row(num);
  }
}

module.exports.refreshDropPoint = refreshDropPoint;

function update(ts) {
  const _ts = Date.now() / 1000;

  $.ajax({
    type: 'POST',
    url: api_url,
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
