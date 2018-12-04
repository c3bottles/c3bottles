{% include "js/base.js" %}

var mapObj = map.initializeMap(mapSource);

mapObj.setView([{{ lat }}, {{ lng }}], 4);
map.setLevel({{ level }});

create.initializeCreation(mapObj);
create.drawNewDp({{ lat }}, {{ lng }});

if (!$(".alert-danger").length) {
    create.setInfoFromMarker({"lat": {{ lat }}, "lng": {{ lng }}});
}
