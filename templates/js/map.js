var drop_points = {{ all_dps_json|safe }};

var create_dp_url = "{{ url_for('manage.create') }}";
var hash = location.hash.substr(1).split("/");

var mapObj = map.initializeMap();

if (hash.length === 4 || hash.length === 5) {
    map.setLevel(hash[0]);
    mapObj.setView([hash[1], hash[2]], hash[3]);
    if (hash.length === 5) {
        var category = parseInt(hash[4]);
        if (Number.isInteger(category)) {
            map.setCategory(category);
        }
    }
} else {
    map.setLevel(0);
    map.setDefaultView();
}

var updateHash = function() {
    let hash =
        "#" + map.getLevel() + "/" + mapObj.getCenter().lat.toPrecision(7) +
        "/" + mapObj.getCenter().lng.toPrecision(7) + "/" + mapObj.getZoom();
    if (map.getCategory() > -1) {
        hash += "/" + map.getCategory();
    }
    location.hash = hash;
}

mapObj.on("moveend", updateHash);
mapObj.on("zoomend", updateHash);

var pane_on_click = "report";

{% if current_user.can_edit: %}
map.allowDpCreation();
{% endif %}
