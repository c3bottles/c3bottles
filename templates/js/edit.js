var drop_points = {{ all_dps_json|safe }};
var mapObj = map.initializeMap()
create.initializeCreation(mapObj);

var lat = {{ dp.lat }};
var lng = {{ dp.lng }};

mapObj.setView([{{ dp.lat }}, {{ dp.lng }}], 3);
map.setLevel({{ dp.level }});

create.drawNewDp({{ dp.lat }}, {{ dp.lng }});
