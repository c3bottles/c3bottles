{% include "js/dp.js" %}
var imgdir = "{{ url_for('static', filename='img') }}";
init_map()
init_dp_creation();
var lat = {{ dp.lat }};
var lng = {{ dp.lng }};
map.setView([{{ dp.lat }}, {{ dp.lng }}], 3);
set_map_level({{ dp.level }});
redraw_markers();
draw_new_dp({{ dp.lat }}, {{ dp.lng }});
