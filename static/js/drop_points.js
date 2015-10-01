var last_update = Date.now()/1000;

function refresh_drop_points() {
    return $.ajax({
        type: "POST",
        url: apiurl,
        data: {
            action: "dp_json",
            ts: last_update
        },
        success: function (response) {
            last_update = Date.now() / 1000;
            drop_points = $.extend(drop_points, response);
            if (typeof map != "undefined") {
                for (var num in response) {
                    redraw_marker(num, response[num].last_state);
                }
            }
        },
        complete: function () {
            setTimeout(function() { refresh_drop_points() }, 120000);
        },
        dataType: "json"
    });
}

setTimeout(function() { refresh_drop_points() }, 120000);

/* vim: set expandtab ts=4 sw=4: */
