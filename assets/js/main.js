global.$ = global.jQuery = require("jquery");
require("bootstrap");
global.stats = require("./stats.js");

var csrftoken = $('meta[name=csrf_token]').attr('content');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
