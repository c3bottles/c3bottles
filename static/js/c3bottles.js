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

/* vim: set expandtab ts=4 sw=4: */
