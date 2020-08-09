const map = require('../common/map');

global.create = require('../common/create');

require('../common/refresh');

global.drop_points = $.parseJSON($('meta[name=all-drop-points]').attr('content'));

const dropPointInfo = $('meta[name=drop-point-info]');

const mapObj = map.initializeMap();

mapObj.setView([dropPointInfo.data('lat'), dropPointInfo.data('lng')], 3);
map.setLevel(dropPointInfo.data('level'));

create.initializeCreation(mapObj);
create.drawNewDp(dropPointInfo.data('lat'), dropPointInfo.data('lng'));
