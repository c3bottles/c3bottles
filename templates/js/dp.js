var apiurl = "{{ url_for('api.process') }}";
var drop_points = {{ all_dps_json|safe }};
init_drop_point_refreshing();
