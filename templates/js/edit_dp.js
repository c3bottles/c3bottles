{% include "js/dp.js" %}
var imgdir = "{{ url_for('static', filename='img') }}";
init_map()
init_dp_creation();
var lat = {{ lat }};
var lng = {{ lng }};
map.setView([{{ lat }}, {{ lng }}], 3);
set_map_level({{ dp.level }});
redraw_markers();
draw_new_dp({{ lat }}, {{ lng }});
