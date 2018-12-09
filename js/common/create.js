const $ = require('jquery');
const L = require('leaflet');

const map = require('./map');

let mapObj;
let newMarker;

function setInfoFromMarker(latlng) {
  const lat = latlng.lat.toPrecision(7);
  const lng = latlng.lng.toPrecision(7);

  $('#lat').val(lat);
  $('#lng').val(lng);
}

function getMarker(latlng) {
  const marker = L.marker(latlng, {
    icon: map.getIcon('new', 'CREATED'),
    draggable: true,
  });

  $(mapObj).one('zoomend', () => {
    if (mapObj.hasLayer(marker)) {
      mapObj.removeLayer(marker);
      getMarker(marker._latlng);
    }
  });
  marker.on('drag', () => {
    setInfoFromMarker(marker._latlng);
  });
  mapObj.addLayer(marker);

  return marker;
}

module.exports.setInfoFromMarker = setInfoFromMarker;

module.exports.drawNewDp = function(lat, lng) {
  const latlng = L.latLng(lat, lng);

  newMarker = getMarker(latlng);
  mapObj.setView(newMarker._latlng, 5);
};

module.exports.initializeCreation = function(mapObj_) {
  mapObj = mapObj_;
  mapObj.on('click', e => {
    if (!newMarker) {
      const latlng = e.latlng;

      newMarker = getMarker(latlng);
      setInfoFromMarker(latlng);
    }
  });
};
