const $ = require('jquery');

/*
 * Get all drop points via the API that have changed since the time given.
 */
function update_drop_points(ts) {
  const _ts = Date.now() / 1000;

  $.ajax({
    type: 'POST',
    url: apiurl,
    data: {
      action: 'dp_json',
      ts,
    },
    dataType: 'json',
    success(response) {
      $.extend(true, drop_points, response);
      for (const num in response) {
        refresh_drop_point(num);
      }
    },
    complete() {
      setTimeout(() => {
        update_drop_points(_ts);
      }, 120000);
    },
  });
}

/*
 * Refresh the given drop point in the map, list etc.
 *
 * This function is intended to be called whenever the drop point has changed,
  * either by an update from the API or locally.
 */
global.refresh_drop_point = function(num) {
  if (typeof map != 'undefined') {
    draw_marker(num);
  }
  if (typeof dt != 'undefined') {
    draw_row(num);
  }
};

global.init_drop_point_refreshing = function() {
  const ts = Date.now() / 1000;

  setTimeout(() => {
    update_drop_points(ts);
  }, 120000);
};
