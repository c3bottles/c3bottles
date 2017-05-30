var $ = require("jquery");
var L = require("leaflet");

/*
 * Initialize the map object, add the background layer and draw all the
 * drop points into the map.
 *
 */
global.map = undefined;
global.init_map = function(opts) {
    map = L.map('map', {
        // set this to true when using Openstreetmap
        // what you set here when you are using another
        // map source depends on the copyright situation
        // of that source
        attributionControl: true
    });

    if (opts.enable) {
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
            subdomains: ['a', 'b', 'c'],
            minZoom: 15, // this is a reasonable default for a decent outdoor event
            maxZoom: 18  // this is the maximum zoom level
        }).addTo(map);
        global.default_map_view = function() {
            // set your event coordinates (latitude, longitude, default zoom) here
            map.setView(opts.lat_lng, opts.default_zoom);
        };
    } else {
        L.tileLayer(imgdir + '/tiles/{z}/{x}/{y}.png', {
            // Have a look in static/img/tiles.
            // The directories present there correspond to zoom levels.
            minZoom: 0,
            maxZoom: 6,
            tms: true,
            noWrap: true
        }).addTo(map);
        global.default_map_view = function() {
            map.fitWorld();
        };
    }

    for (var i in drop_points) {
        if (!drop_points[i].removed) {
            draw_marker(i);
        }
    }
};

/*
 * Get an properly sized icon for a given marker type at the current zoom level.
 */
global.get_icon = function(type) {
    var size = 12;
    var zoom = 6 - (map.getMaxZoom() - map.getZoom());
    if (zoom < 1) {
        zoom = 1;
    }
    return L.icon({
        iconSize: [size * zoom, size * zoom],
        iconAnchor: [size * zoom / 2, size * zoom],
        iconUrl: imgdir + '/markers/' + type + '.svg',
        popupAnchor: [0, -size * zoom]
    });
};

/*
 * Enable the drop point creation on the map.
 *
 * This function registers an event on the map that fires when the user clicks
 * somewhere. A new, draggable marker is placed with a popup that allows
 * creation of a drop point in the current location of the marker. If the user
 * clicks on the map away from the marker, the marker is removed.
 *
 */
global.allow_dp_creation_from_map = function() {
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
};

/*
 * Draw the marker for a given drop point.
 *
 * The function first checks if the marker has already been added to the map
 * and removes it if necessary. It then creates a GeoJSON object from the
 * drop point's metadata and draws it into the map. An event is added that
 * triggers re-drawing the marker once the zoom factor changes.
 *
 */
global.draw_marker = function(num) {
    if (map.hasLayer(drop_points[num].layer)) {
        map.removeLayer(drop_points[num].layer);
    }
    drop_points[num].layer = L.geoJson({
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
                return feature.geometry.coordinates[0] !== null &&
                    feature.geometry.coordinates[1] !== null;
            },
            pointToLayer: function (feature, latlng) {
                var marker = L.marker(latlng, {
                    icon: get_icon(feature.properties.last_state)
                });
                marker.on("click",
                    function (e) {
                        var dp = e.target.feature;
                        show_dp_modal(dp.properties.number, pane_on_click);
                    }
                );
                return marker;
            }
    });
    $(map).one("zoomend", function () {
        draw_marker(num);
    });
    map.addLayer(drop_points[num].layer);
};

/* vim: set expandtab ts=4 sw=4: */
