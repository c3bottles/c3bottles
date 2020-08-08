var drop_points = {{ all_dps_json|safe }};
var mapObj = map.initializeMap();

mapObj.setView([{{ dp.lat }}, {{ dp.lng }}], 3);
map.setLevel({{ dp.level }});
