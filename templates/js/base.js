var apiurl = "{{ url_for('api.process') }}";
var imgdir = "{{ url_for('static', filename='img') }}";

{% set map_source = config.get("MAP_SOURCE") %}
var map_source = {
    attribution: "{{ map_source.attribution }}",
    tile_server: "{{ map_source.tile_server }}",
    tile_server_subdomains: {{ map_source.tile_server_subdomains if map_source.tile_server_subdomains else [] }},
    bounds: {{ map_source.bounds if map_source.bounds else "undefined" }},
    initial_view: {{ map_source.initial_view if map_source.initial_view else "undefined" }},
    level_config: {{ map_source.level_config if map_source.level_config else "undefined" }},
    min_zoom: {{ map_source.min_zoom if map_source.min_zoom else 0 }},
    max_zoom: {{ map_source.max_zoom if map_source.max_zoom else 0 }},
    initial_zoom: {{ map_source.initial_zoom if map_source.initial_zoom else 0}},
    simple_crs: {{ map_source.simple_crs|lower if map_source.simple_crs else "false" }},
    hack_257px: {{ map_source.hack_257px|lower if map_source.hack_257px else "false" }}
};

var drop_points = {{ all_dps_json|safe }};

init_drop_point_refreshing();

