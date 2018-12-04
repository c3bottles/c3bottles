{% include "js/base.js" %}

var mapObj = map.initializeMap(mapSource);

mapObj.setView([{{ dp.lat }}, {{ dp.lng }}], 3);
map.setLevel({{ dp.level }});
