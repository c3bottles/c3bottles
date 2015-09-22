$("body").on("click", "a[data-toggle=collapse]", function () {
    var _self = $(this);
    var _group = _self.parent().parent().parent();
    var _button = _group.children("button");
    var _target = $(_self.attr("data-target"));
    if (_target.hasClass("in")) {
        _self.parent().removeClass("active");
    } else {
        _self.parent().addClass("active");
    }
    if (_group.find("li.active").length > 0) {
        _button.removeClass("btn-default").addClass("btn-primary");
    } else {
        _button.removeClass("btn-primary").addClass("btn-default");
    }
});

$(".dp_modal").on("show.bs.modal", function (e) {
    var _tr = $(e.relatedTarget).parent().parent();
    var _details = _tr.data("details");
    for (var key in _details) {
        $(".modal_dp_" + key).text(_details[key]);
    }
    $("#modal_dp_link").attr("href", _tr.data("href"));
});

$(".dp_modal").on("hidden.bs.modal", function () {
    $(this).removeData("bs.modal");
});

var report_states = {
    ".report-default": "DEFAULT",
    ".report-nocrates": "NO_CRATES",
    ".report-empty": "EMPTY",
    ".report-somebottles": "SOME_BOTTLES",
    ".report-reasonablyfull": "REASONABLY_FULL",
    ".report-full": "FULL",
    ".report-overflow": "OVERFLOW"
};

$.each(report_states, function (cls, state) {
    $(cls).on("click", function () {
        report_dp($(".modal_dp_number").first().text(), state);
    });
});

function report_dp(num, state) {
    $("#dp_report_modal").modal("hide");
    $.ajax({
        type: "POST",
        url: apiurl,
        data: {
            action: "report",
            dp_number: num,
            state: state
        },
        success: function () {
            var alert = $("<div></div>")
                .addClass("alert alert-success collapse")
                .html("<button type=\"button\" class=\"close alert-hide\">\
                        <span aria-hidden=\"true\">&times;</span></button>\
                        <strong>Thank you!</strong> Your report has been\
                        received successfully and the bottle collection\
                        team is on the way.");
            $("#alerts").append(alert);
            $(".alert-hide").on("click", function () {
                $(this).parent().slideUp();
            });
            alert.slideDown();
        },
        error: function (response) {
            var alert = $("<div></div>")
                .addClass("alert alert-danger collapse")
                .html("<button type=\"button\" class=\"close alert-hide\">\
                        <span aria-hidden=\"true\">&times;</span></button>\
                        <strong>Oh no!</strong> An error occured while\
                        processing your report: " + response.responseText);
            $("#alerts").append(alert);
            $(".alert-hide").on("click", function () {
                $(this).parent().slideUp();
            });
            alert.slideDown();
        }
    });
}

var visit_actions = {
    ".visit-emptied": "EMPTIED",
    ".visit-addedcrates": "ADDED_CRATE",
    ".visit-removedcrates": "REMOVED_CRATE",
    ".visit-relocated": "RELOCATED",
    ".visit-removed": "REMOVED",
    ".visit-noaction": "NO_ACTION"
};

$.each(visit_actions, function (cls, action) {
    $(cls).on("click", function () {
        visit_dp($(".modal_dp_number").first().text(), action);
    });
});

function visit_dp(num, action) {
    $("#dp_visit_modal").modal("hide");
    $.ajax({
        type: "POST",
        url: apiurl,
        data: {
            action: "visit",
            dp_number: num,
            maintenance: action
        },
        success: function () {
            var alert = $("<div></div>")
                .addClass("alert alert-success collapse")
                .html("<button type=\"button\" class=\"close alert-hide\">\
                        <span aria-hidden=\"true\">&times;</span></button>\
                        <strong>Thank you!</strong> Your visit has been\
                        logged.");
            $("#alerts").append(alert);
            $(".alert-hide").on("click", function () {
                $(this).parent().slideUp();
            });
            alert.slideDown();
        },
        error: function (response) {
            var alert = $("<div></div>")
                .addClass("alert alert-danger collapse")
                .html("<button type=\"button\" class=\"close alert-hide\">\
                        <span aria-hidden=\"true\">&times;</span></button>\
                        <strong>Oh no!</strong> An error occured while\
                        processing your visit: " + response.responseText);
            $("#alerts").append(alert);
            $(".alert-hide").on("click", function () {
                $(this).parent().slideUp();
            });
            alert.slideDown();
        }
    });
}

/* vim: set expandtab ts=4 sw=4: */
