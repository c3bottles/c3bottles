const $ = require('jquery');

const api_url = $('meta[name="endpoint"]').data('api');
const refreshInterval = 30000;

function update(ts) {
  const _ts = Math.floor(Date.now() / 1000);

  $.get(`${api_url}all_dp.json`, { ts, }).then(response => {
    global.drop_points = global.drop_points || [];
    $.extend(true, drop_points, response);
    if (typeof(global.refreshDropPoint) === 'function') {
      for (const num in response) {
        global.refreshDropPoint(num);
      }
    }
    setTimeout(() => {
      update(_ts);
    }, refreshInterval);
  });
}

const ts = Math.floor(Date.now() / 1000);

setTimeout(() => {
  update(ts);
}, refreshInterval);
