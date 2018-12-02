{% include "js/base.js" %}

var create_dp_url = "{{ url_for('manage.create') }}";
var hash = location.hash.substr(1).split("/");

init_map();
if (hash.length === 4 || hash.length === 5) {
    set_map_level(hash[0]);
    redraw_markers();
    map.setView([hash[1], hash[2]], hash[3]);
    if (hash.length === 5) {
        var category = parseInt(hash[4]);
        if (Number.isInteger(category)) {
            setMapCategory(category);
        }
    }
} else {
    if (typeof default_map_view === "function") {
        default_map_view();
    }
}
var update_hash = function() {
    let hash =
        "#" + current_level + "/" + map.getCenter().lat.toPrecision(7) +
        "/" + map.getCenter().lng.toPrecision(7) + "/" + map.getZoom();
    if (map_category > -1) {
        hash += "/" + map_category;
    }
    location.hash = hash;
}
map.on("moveend", update_hash);
map.on("zoomend", update_hash);
var pane_on_click = "report";
{% if current_user.can_edit: %}
allow_dp_creation_from_map();
{% endif %}
