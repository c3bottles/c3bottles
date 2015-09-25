var new_dp_marker = null;

var used_dp_numbers = [];
for (var i in all_dps_geojson) {
    used_dp_numbers.push(all_dps_geojson[i].properties.number);
}

function get_marker(latlng) {
    var marker = L.marker(latlng, {
        icon: get_icon("NEW"),
        draggable: true
    });
    $(map).one("zoomend", function (e) {
        if (map.hasLayer(marker)) {
            map.removeLayer(marker);
            get_marker(marker._latlng);
        }
    });
    marker.on("drag", function () {
        set_info_from_marker(this._latlng);
    });
    map.addLayer(marker);
    return marker;
}

function draw_new_dp(lat, lng) {
    var latlng = L.latLng(lat, lng);
    new_dp_marker = get_marker(latlng);
    map.setView(new_dp_marker._latlng, 5);
}

function set_info_from_marker(latlng) {
    lat = latlng.lat.toFixed(2);
    lng = latlng.lng.toFixed(2);
    $("#lat").val(lat);
    $("#lng").val(lng);
    var room = get_room([lng, lat]);
    if (room != null) {
        $("#location_description").val(room.name);
        $("#dp_number").val(get_next_free_dp_num(room.level));
        $("input[name='level'][value=" + room.level + "]").prop("checked", true);
    } else {
        var level = get_level([lng, lat]);
        if (level != null) {
            $("#dp_number").val(get_next_free_dp_num(level));
            $("input[name='level'][value=" + level + "]").prop("checked", true);
        }
    }
}

function get_next_free_dp_num(level) {
    for (var i = level*100; i < level*100 + 100; i++) {
        if ($.inArray(i, used_dp_numbers) < 0) {
            return i;
        }
    }
}

map.on("click", function (e) {
    if (!new_dp_marker) {
        var latlng = e.latlng;
        new_dp_marker = get_marker(latlng);
        set_info_from_marker(latlng);
    }
});

$(".btn-number").click(function () {
    var field = $(this).data("field");
    var type = $(this).data("type");
    var input = $("input[name='" + field + "']");
    var val = parseInt(input.val());
    if (!isNaN(val)) {
        if (type == "minus") {
            if (val > input.attr("min")) {
                input.val(val-1).change();
            }
            if (parseInt(input.val()) == input.attr("min")) {
                $(this).attr("disabled", true);
            }
        } else if (type == "plus") {
            if (val < input.attr("max")) {
                input.val(val+1).change();
            }
            if (parseInt(input.val()) == input.attr("max")) {
                $(this).attr("disabled", true);
            }

        }
    } else {
        input.val(0);
    }
});

$(".input-number").focusin(function () {
    $(this).data("old", $(this).val());
});

$(".input-number").change(function () {
    var min = parseInt($(this).attr("min"));
    var max = parseInt($(this).attr("max"));
    var val = parseInt($(this).val());
    var name = $(this).attr("name");
    if (val >= min) {
        $(".btn-number[data-type='minus'][data-field='" + name + "']").removeAttr("disabled");
    } else {
        alert("Sorry, the minimum value was reached.");
        $(this).val($(this).data("old"));
    }
    if (val <= max) {
        $(".btn-number[data-type='plus'][data-field='" + name + "']").removeAttr("disabled");
    } else {
        alert("Sorry, the maximum value was reached.");
        $(this).val($(this).data("old"));
    }
});

$(".input-number").keydown(function (e) {
    // Allow: backspace, delete, tab, escape, enter and .
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
        // Allow: Ctrl+A
        (e.keyCode == 65 && e.ctrlKey === true) ||
        // Allow: home, end, left, right
        (e.keyCode >= 35 && e.keyCode <= 39)) {
        // let it happen, don't do anything
        return;
    }
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
});

/* vim: set expandtab ts=4 sw=4: */
