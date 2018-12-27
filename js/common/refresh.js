const $ = require('jquery');

const refreshInterval = 30000;

function update(ts) {
  const _ts = Date.now() / 1000;

  $.post('/api/all_dp.json', {
    ts,
  }).then(response => {
    global.drop_points = global.drop_points || [];
    $.extend(true, drop_points, response);
    for (const num in response) {
      global.refreshDropPoint(num);
    }
    setTimeout(() => {
      update(_ts);
    }, refreshInterval);
  });
}

const ts = Date.now() / 1000;

setTimeout(() => {
  update(ts);
}, refreshInterval);
