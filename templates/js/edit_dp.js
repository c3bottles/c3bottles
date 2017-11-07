{% from "macros/map.js" import init_map %}
{% include "js/dp.js" %}
var imgdir = "{{ url_for('static', filename='img') }}";
{{ init_map() }}
init_dp_creation();
var lat = {{ lat }};
var lng = {{ lng }};
map.setView([{{ lat }}, {{ lng }}], 5);
draw_new_dp({{ lat }}, {{ lng }});
