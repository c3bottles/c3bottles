const map = require('../common/map');

global.drop_points = $.parseJSON($('meta[name=all-drop-points]').attr('content'));
global.createUrl = $('meta[name=create-options').data('createUrl');
const userCanEdit = $('meta[name=create-options').data('userCanEdit');

global.pane_on_click = 'report';

let hash = location.hash.substr(1).split('/');

const mapObj = map.initializeMap();

if (hash.length === 4 || hash.length === 5) {
    map.setLevel(hash[0]);
    mapObj.setView([hash[1], hash[2]], hash[3]);
    if (hash.length === 5) {
        let category = parseInt(hash[4]);
        if (Number.isInteger(category)) {
            map.setCategory(category);
        }
    }
} else {
    map.setLevel(0);
    map.setDefaultView();
}

const updateHash = function() {
    let hash =
        '#' + map.getLevel() + '/' + mapObj.getCenter().lat.toPrecision(7) +
        '/' + mapObj.getCenter().lng.toPrecision(7) + '/' + mapObj.getZoom();
    if (map.getCategory() > -1) {
        hash += '/' + map.getCategory();
    }
    location.hash = hash;
}

mapObj.on('moveend', updateHash);
mapObj.on('zoomend', updateHash);

if (userCanEdit) {
    map.allowDpCreation();
}
