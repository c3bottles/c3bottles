{% import "macros/states.html" as states %}
{{ states.label_js() }}
stats.draw_drop_points_by_state({{ stats.drop_points_by_state|tojson }});
stats.draw_reports_by_state({{ stats.reports_by_state|tojson }});
