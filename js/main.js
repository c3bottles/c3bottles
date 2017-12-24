global.$ = global.jQuery = require('jquery');
require('bootstrap');
global.stats = require('./stats.js');

const csrftoken = $('meta[name=csrf_token]').attr('content');

$.ajaxSetup({
  beforeSend(xhr, settings) {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
    }
  },
});
