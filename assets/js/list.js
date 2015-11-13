var $ = require("jquery");
require("datatables-bootstrap3-plugin");

var icon_details = $("<span></span>").addClass("clickable glyphicon glyphicon-search dp_modal details");
var icon_report = $("<span></span>").addClass("clickable glyphicon glyphicon-bullhorn dp_modal report");
var icon_visit = $("<span></span>").addClass("clickable glyphicon glyphicon-wrench dp_modal visit");

function get_table_data() {
    var arr = [];
    for (var num in drop_points) {
        arr.push(drop_points[num]);
    }
    return arr;
}

global.dt = undefined;
global.init_table = function() {
    dt = $('#dp_list').DataTable({
        data: get_table_data(),
        order: [[6, "desc"]],
        createdRow: function(row, data) {
            drop_points[data.number]["row"] = row;
        },
        columns: [
            {
                data: "number"
            },
            {
                data: null,
                render: function (data) {
                    if (data.description) {
                        return data.description;
                    } else {
                        return "somewhere on level " + data.level
                    }
                }
            },
            {
                data: null,
                render: function (data, type) {
                    if (type == "sort") {
                        return labels[data.last_state][0];
                    } else {
                        return labels[data.last_state][1][0].outerHTML;
                    }
                }
            },
            {
                data: null, orderable: false, defaultContent: "",
                createdCell: function (td, cd, rd) {
                    rd["details_cell"] = td;
                },
                render: function(data) {
                    var my_icon = icon_details.clone();
                    my_icon.click(function () {
                        show_dp_modal(data.number, "details");
                    });
                    $(data.details_cell).empty().append(my_icon);
                }
            },
            {
                data: null, orderable: false, defaultContent: "",
                createdCell: function (td, cd, rd) {
                    rd["report_cell"] = td;
                },
                render: function(data) {
                    var my_icon = icon_report.clone();
                    my_icon.click(function () {
                        show_dp_modal(data.number, "report");
                    });
                    $(data.report_cell).empty().append(my_icon);
                }

            },
            {
                data: null, orderable: false, defaultContent: "",
                createdCell: function (td, cd, rd) {
                    rd["visit_cell"] = td;
                },
                render: function(data) {
                    var my_icon = icon_visit.clone();
                    my_icon.click(function () {
                        show_dp_modal(data.number, "visit");
                    });
                    $(data.visit_cell).empty().append(my_icon);
                }
            },
            {
                data: null, sort: "desc", className: "hidden-xs",
                render: function(data, type) {
                    var prio = (Date.now() / 1000 - data["base_time"]) *
                        data["priority_factor"];
                    drop_points[data.number].priority = prio.toFixed(2);
                    return prio.toFixed(2);
                }
            },
            {
                data: "reports_new", className: "hidden-xs"
            }
        ]
    });

    setTimeout(function() { redraw_table(); }, 10000);

}

function draw_row(num) {
    if (drop_points[num] && drop_points[num]["row"]) {
        dt.row(drop_points[num].row).data(drop_points[num]).draw(false);
    } else if (drop_points[num]) {
        dt.row.add(drop_points[num]).draw(false);
    }
}

function redraw_table() {
    dt.rows().invalidate().draw(false);
    setTimeout(function() { redraw_table(); }, 10000);
}

/* vim: set expandtab ts=4 sw=4: */
