var map = L.map('map', {
    attributionControl: false
}).fitWorld();
L.tileLayer(tiledir + '/{z}/{x}/{y}.png', {
    // Have a look in static/img/tiles.
    // The directories present there correspond to zoom levels.
    minZoom: 0,
    maxZoom: 6,
    tms: true,
    noWrap: true
}).addTo(map);

/* vim: set expandtab ts=4 sw=4: */
