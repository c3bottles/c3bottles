/*
 * Initialize the map object.
 *
 */
var map = L.map('map', {
    attributionControl: false
}).fitWorld();

/*
 * Add the background layer to the map.
 *
 */
L.tileLayer(imgdir + '/tiles/{z}/{x}/{y}.png', {
    // Have a look in static/img/tiles.
    // The directories present there correspond to zoom levels.
    minZoom: 0,
    maxZoom: 6,
    tms: true,
    noWrap: true
}).addTo(map);

/*
 * Get an properly sized icon for a given marker type at the current zoom level.
 *
 */
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

/*
 * Enable the drop point creation on the map.
 *
 * This function registers an event on the map that fires when the user clicks
 * somewhere. A new, draggable marker is placed with a popup that allows
 * creation of a drop point in the current location of the marker. If the user
 * clicks on the map away from the marker, the marker is removed.
 *
 */
function allow_dp_creation_from_map() {
    map.on("click", function (e) {
        var latlng = e.latlng;
        function get_marker(latlng) {
            var marker = L.marker(latlng, {
                icon: get_icon("CREATED"),
                draggable: true
            });
            $(map).one("zoomend", function () {
                if (map.hasLayer(marker)) {
                    map.removeLayer(marker);
                    get_marker(marker._latlng);
                }
            });
            $(map).one("click", function () {
                map.removeLayer(marker);
            });
            var lat = marker._latlng.lat.toFixed(2);
            var lng = marker._latlng.lng.toFixed(2);
            marker.bindPopup(L.popup({closeButton: false}).setContent(
                "<a class='btn btn-primary' href=\'" + create_dp_url + "/" +
                lat + "/" + lng + "' style='color: #fff;'>" +
                "Create a new drop point" +
                "</a>"
            ));
            marker.on("dragend", function () {
                var lat = this._latlng.lat.toFixed(2);
                var lng = this._latlng.lng.toFixed(2);
                this._popup.setContent(
                    "<a class='btn btn-primary' href=\'" + create_dp_url + "/" +
                    lat + "/" + lng + "' style='color: #fff;'>" +
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

/*
 * Draw the marker for a given drop point.
 *
 * The function first checks if the marker has already been added to the map
 * and removes it if necessary. It then creates a GeoJSON object from the
 * drop point's metadata and draws it into the map. An event is added that
 * triggers re-drawing the marker once the zoom factor changes.
 *
 */
function draw_marker(num) {
    if (map.hasLayer(drop_points[num]["layer"])) {
        map.removeLayer(drop_points[num]["layer"]);
    }
    drop_points[num]["layer"] = L.geoJson({
            type: "Feature",
            geometry: {
                type: "Point",
                coordinates: [drop_points[num].lng, drop_points[num].lat]
            },
            properties: {
                last_state: drop_points[num].last_state,
                number: parseInt(num)
            }
        }, {
            filter: function (feature) {
                return feature.geometry.coordinates[0] != null &&
                    feature.geometry.coordinates[1] != null;
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
        draw_marker(num);
    });
    map.addLayer(drop_points[num]["layer"]);
}

/*
 * Redraw the marker of a given drop point for a new state.
 *
 */
function redraw_marker(num, state) {
    drop_points[num].last_state = state;
    draw_marker(num);
}

/*
 * Draw all drop points into the map.
 *
 */
for (var i in drop_points) {
    draw_marker(i);
}

/* vim: set expandtab ts=4 sw=4: */
