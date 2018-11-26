{% include "js/dp.js" %}
var imgdir = "{{ url_for('static', filename='img') }}";
init_map()
map.setView([{{ dp.lat }}, {{ dp.lng }}], 3);
set_map_level({{ dp.level }});
redraw_markers();
