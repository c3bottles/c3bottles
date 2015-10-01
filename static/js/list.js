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

var dt = $('#dp_list').DataTable({
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
            render: function (data) {
                return labels[data.last_state][0].outerHTML;
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
            data: "priority", sort: "desc",
            render: function(data) {
                return data.toFixed(2);
            }
        },
        {
            data: "reports_new"
        }
    ]
});

function draw_row(num) {
    dt.row(drop_points[num].row).data(drop_points[num]).draw()
}

/* vim: set expandtab ts=4 sw=4: */
