var $ = require("jquery");
var Chart = require("chart.js");

Chart.defaults.global.animation = false;
Chart.defaults.Doughnut.percentageInnerCutout = 40;

exports.draw_drop_points_by_state = function(_data) {
    data = []; 
    for (var state in _data) {
        data.push({
            value: _data[state],
            color: $(labels[state][1]).css("background-color"),
            label: $(labels[state][1]).text()
        }); 
    }   
    var ctx = $("#drop_points_by_state").get(0).getContext("2d");
    new Chart(ctx).Doughnut(data);
};

exports.draw_reports_by_state = function(_data) {
    data = [];
    for (var state in _data) {
        data.push({
            value: _data[state],
            color: $(labels[state][1]).css("background-color"),
            label: $(labels[state][1]).text()
        });
    }
    var ctx = $("#reports_by_state").get(0).getContext("2d");
    new Chart(ctx).Doughnut(data);
};

/* vim: set expandtab ts=4 sw=4: */
