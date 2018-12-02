{% include "js/base.js" %}

var mapObj = map.initializeMap(mapSource)
create.initializeCreation(mapObj);

var lat = {{ dp.lat }};
var lng = {{ dp.lng }};

mapObj.setView([{{ dp.lat }}, {{ dp.lng }}], 3);
map.setLevel({{ dp.level }});

create.drawNewDp({{ dp.lat }}, {{ dp.lng }});
