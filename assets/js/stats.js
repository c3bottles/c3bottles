var $ = require("jquery");
var Chart = require("chart.js");


var options = {
    animation: false,
    legend: { display: false },
    tooltips: { bodyFontSize: 20 }
}

exports.draw_drop_points_by_state = function(_data) {
    var d = [];
    var l = [];
    var c = [];
    for (var state in labels) {
        if (typeof _data[state] !== "number" || _data[state] === 0) {
            continue;
        }
        d.push(_data[state]);
        c.push(labels[state][2]);
        l.push($(labels[state][1]).text());
    }
    global.data = {
        d: d,
        l: l,
        c: c
    }
    global.chart = new Chart($("#drop_points_by_state"), {
        type: "doughnut",
        data: {
            labels: l,
            datasets: [{
                data: d,
                backgroundColor: c,
                hoverBackgroundColor: c
            }]
        },
        options: options
    });
};

exports.draw_reports_by_state = function(_data) {
    var d = [];
    var l = [];
    var c = [];
    for (var state in labels) {
        if (typeof _data[state] !== "number" || _data[state] === 0) {
            continue;
        }
        d.push(_data[state]);
        c.push(labels[state][2]);
        l.push($(labels[state][1]).text());
    }
    new Chart($("#reports_by_state"), {
        type: "doughnut",
        data: {
            labels: l,
            datasets: [{
                data: d,
                backgroundColor: c,
                hoverBackgroundColor: c
            }]
        },
        options: options
    });
};

/* vim: set expandtab ts=4 sw=4: */
