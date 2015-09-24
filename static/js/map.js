function get_icon(type) {
    var size = 12;
    var zoom = map.getZoom();
    return L.icon({
        iconSize: [size * zoom, size * zoom],
        iconAnchor: [size * zoom / 2, size * zoom],
        iconUrl: imgdir + '/markers/' + type + '.svg'
    });
}

var map = L.map('map', {
    attributionControl: false
}).fitWorld();

map.on("click", function (e) {
    var latlng = e.latlng;

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
        $(map).one("click", function() {
            map.removeLayer(marker);
        });
        marker.on("click", function() {
            var latlng = this._latlng;
            // TODO: popup, etc.
            alert("marker is at " + latlng.lat + "," + latlng.lng);
        });
        map.addLayer(marker);
    }

    get_marker(latlng);
});

L.tileLayer(imgdir + '/tiles/{z}/{x}/{y}.png', {
    // Have a look in static/img/tiles.
    // The directories present there correspond to zoom levels.
    minZoom: 0,
    maxZoom: 6,
    tms: true,
    noWrap: true
}).addTo(map);

function get_dp_layer() {
    var layer = L.geoJson(all_dps_geojson, {
        filter: function (feature) {
            return feature.geometry.coordinates[0] != null &&
                feature.geometry.coordinates[0] != null;
        },
        pointToLayer: function (feature, latlng) {
            var marker = L.marker(latlng, {
                icon: get_icon(feature.properties.last_state)
            });
            marker.on("click",
                function (e) {
                    var dp = e.target.feature;
                    show_dp_modal(dp.properties.number, "report");
                }
            );
            return marker;
        }
    });
    $(map).one("zoomend", function () {
        map.removeLayer(layer);
        dp_layer = get_dp_layer();
        map.addLayer(dp_layer);
    });
    return layer;
}

var dp_layer = get_dp_layer();
map.addLayer(dp_layer);

/* vim: set expandtab ts=4 sw=4: */
