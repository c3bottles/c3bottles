/*
 * Get all drop points via the API that have changed since the time given.
 */
function update_drop_points(ts) {
    $.ajax({
        type: "POST",
        url: apiurl,
        data: {
            action: "dp_json",
            ts: ts
        },
        success: function (response) {
            last_update = Date.now() / 1000;
            drop_points = $.extend(drop_points, response);
            for (var num in response) {
                refresh_drop_point(num);
            }
        },
        complete: function () {
            setTimeout(function() {
                update_drop_points(Date.now()/1000);
            }, 120000);
        },
        dataType: "json"
    });
}

/*
 * Refresh the given drop point in the map, list etc.
 *
 * This function is intended to be called whenever the drop point has changed,
  * either by an update from the API or locally.
 */
function refresh_drop_point(num) {
    if (typeof map != "undefined") {
        redraw_marker(num, drop_points[num].last_state);
    }
}

setTimeout(function() {
    update_drop_points(Date.now()/1000);
}, 120000);

/* vim: set expandtab ts=4 sw=4: */
