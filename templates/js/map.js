{% include "js/dp.js" %}
var create_dp_url = "{{ url_for("create") }}";
var imgdir = "{{ url_for('static', filename='img') }}";
var hash = location.hash.substr(1).split("/");
init_map();
if (hash.length === 4) {
    set_map_level(hash[0]);
    map.setView([hash[1], hash[2]], hash[3]);
} else {
    if (typeof default_map_view === "function") {
        default_map_view();
    }
}
var update_hash = function() {
    location.hash =
        "#" + current_level + "/" + map.getCenter().lat.toFixed(2) +
        "/" + map.getCenter().lng.toFixed(2) + "/" + map.getZoom();
}
map.on("moveend", update_hash);
map.on("zoomend", update_hash);
var pane_on_click = "{{ "visit" if g.user.is_authenticated and g.user.can_visit else "report" }}"
{% if g.user.is_authenticated and g.user.can_edit: %}
allow_dp_creation_from_map();
{% endif %}
