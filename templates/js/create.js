{% include "js/base.js" %}

init_map();
set_map_level({{ level }});
map.setView([{{ lat }}, {{ lng }}], 4);
init_dp_creation();
draw_new_dp({{ lat }}, {{ lng }});
if (!$(".alert-danger").length) {
    set_info_from_marker({"lat": {{ lat }}, "lng": {{ lng }}});
}
