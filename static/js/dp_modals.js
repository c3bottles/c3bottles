/*
 * When hiding any of the drop point modals (details, reporting, visiting),
 * the modal must be destroyed to be re-constructed on the next show instead
 * of simply hiding it and displaying the same instance again.
 *
 */
$("#dp_modal").on("hidden.bs.modal", function () {
    $(this).removeData("bs.modal");
});

/*
 * Add an event handler to all the report buttons.
 *
 */
$(".report-button").each(function () {
    $(this).on("click", function (e) {
        report_dp($(".modal_dp_number").first().text(), $(e.target).val());
    });
});

/*
 * Report a drop point through the AJAX API.
 *
 * The state of the drop point in question is sent through the API and the
 * modal with the buttons is hidden. After the API request has been finished,
 * an alert indicating success or failure is displayed.
 *
 */
function report_dp(num, state) {
    $("#dp_modal").modal("hide");
    $.ajax({
        type: "POST",
        url: apiurl,
        data: {
            action: "report",
            number: num,
            state: state
        },
        dataType: "json",
        success: function (response) {
            add_alert(
                "success",
                "Thank you!",
                "Your report has been received successfully."
            );
            $.extend(true, drop_points, response);
            refresh_drop_point(num);
        },
        error: function (response) {
            var errors = $.parseJSON(response.responseText);
            for (var i in errors) {
                for (var key in errors[i]) {
                    add_alert(
                        "danger",
                        "Oh no!",
                        "An error occurred while processing your report: " +
                        errors[i][key]
                    );
                }
            }
        }
    });
}

/*
 * Add an event handler to all the visit buttons.
 */
$(".visit-button").each(function () {
    $(this).on("click", function (e) {
        visit_dp($(".modal_dp_number").first().text(), $(e.target).val());
    });
});

/*
 * Log the visit of a drop point through the AJAX API.
 *
 * The action performed when visiting the drop point is sent through the API
 * and the modal with the buttons is hidden. After the API request has been
 * finished, an alert indicating success or failure is displayed.
 *
 */
function visit_dp(num, action) {
    if (action == "EMPTIED") {
        $("#dp_modal").modal("hide");
    } else {
        show_dp_modal_pane("report");
    }
    $.ajax({
        type: "POST",
        url: apiurl,
        data: {
            action: "visit",
            number: num,
            maintenance: action
        },
        dataType: "json",
        success: function (response) {
             add_alert(
                "success",
                 "Thank you!",
                 "Your visit has been logged successfully."
             );
            $.extend(true, drop_points, response);
            refresh_drop_point(num);
        },
        error: function (response) {
            var errors = $.parseJSON(response.responseText);
            for (var i in errors) {
                for (var key in errors[i]) {
                    add_alert(
                        "danger",
                        "Oh no!",
                        "An error occurred while processing your visit: " +
                        errors[i][key]
                    );
                }
            }
        }
    });
}

/*
 * When showing any pane of the drop point modal (details, reporting,
 * visiting), all elements displaying details of the drop point in question are
 * filled with the correct details before the modal is made visible to the user.
 * All the details are read from the drop point JSON object.
 *
 * In addition, the correct pane of the modal is selected and the modal is
 * shown.
 *
 */
function show_dp_modal(num, pane) {
    var details = drop_points[num]
    for (var key in details) {
        $(".modal_dp_" + key).text(details[key]);
    }
    var link = $("#modal_dp_link");
    link.attr("href", link.data("baseurl") + "/" + num);
    show_dp_modal_pane(pane);
    $("#dp_modal").modal("show");
}

/*
 * Select a specific given pane in the drop point modal.
 *
 */
function show_dp_modal_pane(pane) {
    for (var arr = ["details", "report", "visit"], i = 0; i < arr.length; i++) {
        $("#dp_modal_" + arr[i] + "_tab").removeClass("active");
        $("#dp_modal_" + arr[i] + "_link").removeClass("active");
    }
    $("#dp_modal_" + pane + "_tab").addClass("active");
    $("#dp_modal_" + pane + "_link").addClass("active");
}

function add_alert(type, title, message) {
    var alert = $("<div></div>")
        .addClass("alert alert-" + type + " collapse")
        .html("<button type=\"button\" class=\"close alert-hide\">\
                        <span aria-hidden=\"true\">&times;</span></button>\
                        <strong>" + title + "</strong> " + message);
    $("#alerts").prepend(alert);
    $(".alert-hide").on("click", function () {
        $(this).parent().slideUp();
    });
    alert.slideDown();
    setTimeout(function() { alert.slideUp() }, 5000);
}

/* vim: set expandtab ts=4 sw=4: */
