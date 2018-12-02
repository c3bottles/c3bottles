var apiurl = "{{ url_for('api.process') }}";
var imgdir = "{{ url_for('static', filename='img') }}";

{% set map_source = config.get("MAP_SOURCE", {}) %}
var map_source = {
    attribution: "{{ map_source.get('attribution', '') }}",
    tileserver: "{{ map_source.get('tileserver', '') }}",
    tileserver_subdomains: {{ map_source.get("tileserver_subdomains", '[]') }},
    bounds: {{ map_source.get("bounds", "undefined") }},
    initial_view: {{ map_source.get("initial_view", "undefined") }},
    level_config: {{ map_source.get("level_config", "undefined") }},
    min_zoom: {{ map_source.get("min_zoom", 0) }},
    max_zoom: {{ map_source.get("max_zoom", 0) }},
    simple_crs: {{ map_source.get("simple_crs", false)|lower }},
    hack_257px: {{ map_source.get("hack_257px", false)|lower }}
};

var drop_points = {{ all_dps_json|safe }};

init_drop_point_refreshing();

