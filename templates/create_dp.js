{% from "macros.html" import init_map %}
{% include "dp.js" %}
var imgdir = "{{ url_for('static', filename='img') }}";
{{ init_map() }}
init_dp_creation();
{% if lat is not none and lng is not none %}
var lat = {{ lat|round(2) }};
var lng = {{ lng|round(2) }};
if (lat < -90 || lat > 90 || lng < -180 || lng > 180) {
    var alert = $("<div></div>")
            .addClass("alert alert-danger")
            .html("<button type=\"button\" class=\"close alert-hide\">\
                    <span aria-hidden=\"true\">&times;</span></button>\
                    <strong>{{ _("Error!") }}</strong> {{ _("The coordinates given were invalid. Pleae choose a new position from the map.") }}");
        $("#alerts").prepend(alert);
        $(".alert-hide").on("click", function () {
            $(this).parent().slideUp();
        });
} else {
    draw_new_dp({{ lat }}, {{ lng }});
    if (!$(".alert-danger").length) {
        set_info_from_marker({"lat": {{ lat }}, "lng": {{ lng }}});
    }
}
{% endif %}
{% if center_lat is not none and center_lng is not none %}
    map.setView([{{ center_lat }}, {{ center_lng }}], 5);
{% endif %}
