{% from "macros.html" import init_map %}
{% include "dp.js" %}
var imgdir = "{{ url_for('static', filename='img') }}";
{{ init_map() }}
map.setView([{{ dp.get_current_location().lat }}, {{ dp.get_current_location().lng }}], 5);
