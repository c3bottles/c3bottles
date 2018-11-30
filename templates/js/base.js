var apiurl = "{{ url_for('api.process') }}";
var imgdir = "{{ url_for('static', filename='img') }}";

var drop_points = {{ all_dps_json|safe }};

init_drop_point_refreshing();

