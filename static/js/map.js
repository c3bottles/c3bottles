var extent = [0, 0, 5500, 10500];
var projection = new ol.proj.Projection({
    code: "dp_map",
    units: "pixels",
    extent: extent
});

var map = new ol.Map({
    layers: [
        new ol.layer.Image({
            source: new ol.source.ImageStatic({
                url: mapurl,
                projection: projection,
                imageExtent: extent
            })
        })
    ],
    target: 'map',
    view: new ol.View({
              projection: projection,
              center: ol.extent.getCenter(extent),
              zoom: 2
          })
});

/* vim: set expandtab ts=4 sw=4: */
