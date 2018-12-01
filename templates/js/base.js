var apiurl = "{{ url_for('api.process') }}";
var imgdir = "{{ url_for('static', filename='img') }}";

{% set map_source = config.MAP_SOURCE %}
var map_source = {
    attribution: "{{ map_source.get_attribution() }}",
    tile_server: "{{ map_source.tile_server }}",
    bounds: {{ map_source.bounds }},
    level_config: {{ map_source.level_config }},
    min_zoom: {{ map_source.min_zoom }},
    max_zoom: {{ map_source.max_zoom }},
    initial_zoom: {{ map_source.initial_zoom }},
};

var drop_points = {{ all_dps_json|safe }};

init_drop_point_refreshing();

