var $ = require("jquery");
var Chart = require("chart.js");

Chart.defaults.global.animation = false;
Chart.defaults.Doughnut.percentageInnerCutout = 40;

global.draw_drop_points_by_state = function(_data) {
    data = []; 
    for (var state in _data) {
        data.push({
            value: _data[state],
            color: $(labels[state][1]).css("background-color"),
            label: $(labels[state][1]).text()
        }); 
    }   
    console.log(data);
    var ctx = $("#drop_points_by_state").get(0).getContext("2d");
    var chart =  new Chart(ctx).Doughnut(data);
    console.log(ctx);
    console.log(chart);
}

global.draw_reports_by_state = function(_data) {
    data = [];
    for (var state in _data) {
        data.push({
            value: _data[state],
            color: $(labels[state][1]).css("background-color"),
            label: $(labels[state][1]).text()
        });
    }
    console.log(data);
    var ctx = $("#reports_by_state").get(0).getContext("2d");
    var chart =  new Chart(ctx).Doughnut(data);
    console.log(ctx);
    console.log(chart);
}

/* vim: set expandtab ts=4 sw=4: */
