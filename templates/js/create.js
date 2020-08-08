var drop_points = {{ all_dps_json|safe }};
var mapObj = map.initializeMap();

mapObj.setView([{{ lat }}, {{ lng }}], 4);
map.setLevel({{ level }});

create.initializeCreation(mapObj);
create.drawNewDp({{ lat }}, {{ lng }});

if (!$(".alert-danger").length) {
    create.setInfoFromMarker({"lat": {{ lat }}, "lng": {{ lng }}});
}
