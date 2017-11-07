{% from "macros/map.js" import init_map %}
{% include "js/dp.js" %}
var create_dp_url = "{{ url_for("create_dp") }}";
var imgdir = "{{ url_for('static', filename='img') }}";
{{ init_map() }}
var hash = location.hash.substr(1).split("/");
if (hash.length == 3) {
    map.setView([hash[0], hash[1]], hash[2]);
} else {
    if (typeof default_map_view === "function") {
        default_map_view();
    }
}
map.on("moveend", function() {
    location.hash = "#" + map.getCenter().lat.toFixed(2) + "/" +
        map.getCenter().lng.toFixed(2) + "/" + map.getZoom();
});
map.on("zoomend", function() {
    location.hash = "#" + map.getCenter().lat.toFixed(2) + "/" +
        map.getCenter().lng.toFixed(2) + "/" + map.getZoom();
});
var pane_on_click = "{{ "visit" if g.user.is_authenticated and g.user.can_visit else "report" }}"
{% if g.user.is_authenticated and g.user.can_edit: %}
allow_dp_creation_from_map();
{% endif %}
