function get_icon(type) {
    var size = 12;
    var zoom = map.getZoom();
    return L.icon({
        iconSize: [size * zoom, size * zoom],
        iconAnchor: [size * zoom / 2, size * zoom],
        iconUrl: imgdir + '/markers/' + type + '.svg',
        popupAnchor: [0, -size * zoom]
    });
}

var map = L.map('map', {
    attributionControl: false
}).fitWorld();

function allow_dp_creation_from_map() {
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
            $(map).one("click", function () {
                map.removeLayer(marker);
            });
            marker.bindPopup(L.popup({closeButton: false}).setContent(
                "<a class='btn btn-primary' href=\'" + create_dp_url + "/" +
                marker._latlng.lat + "/" + marker._latlng.lng + "' style='color: #fff;'>" +
                "Create a new drop point" +
                "</a>"
            ));
            marker.on("dragend", function () {
                this._popup.setContent(
                    "<a class='btn btn-primary' href=\'" + create_dp_url + "/" +
                    this._latlng.lat + "/" + this._latlng.lng + "' style='color: #fff;'>" +
                    "Create a new drop point" +
                    "</a>"
                );
            });
            map.addLayer(marker);
            return marker;
        }
        var marker = get_marker(latlng);
        marker.openPopup();
    });
}

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