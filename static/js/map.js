var map = L.map('map', {
    attributionControl: false
}).fitWorld();

L.tileLayer(imgdir + '/tiles/{z}/{x}/{y}.png', {
    // Have a look in static/img/tiles.
    // The directories present there correspond to zoom levels.
    minZoom: 0,
    maxZoom: 6,
    tms: true,
    noWrap: true
}).addTo(map);

function get_dp_layer() {
    var dp_layer = L.geoJson(all_dps_geojson, {
        filter: function (feature) {
            return feature.geometry.coordinates[0] != null &&
                feature.geometry.coordinates[0] != null;
        },
        pointToLayer: function (feature, latlng) {
            var zoom = map.getZoom();
            var size = 12;
            var icon = L.icon({
                iconSize: [size*zoom, size*zoom],
                iconAnchor: [size*zoom/2, size*zoom],
                iconUrl: imgdir + '/markers/' + feature.properties.last_state + '.svg'
            });
            var marker = L.marker(latlng, {icon: icon});
            return marker;
        }
    });
    $(map).one("zoomend", function() {
        map.removeLayer(dp_layer);
        map.addLayer(get_dp_layer());
    });
    return dp_layer;
}

map.addLayer(get_dp_layer());

/* vim: set expandtab ts=4 sw=4: */
