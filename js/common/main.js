global.$ = global.jQuery = require('jquery');

require('bootstrap');
require('bootstrap-select');

setTimeout(() => {
  $('.disappear').slideUp();
}, 5000);

$('#login-form-dropdown').on('shown.bs.dropdown', () => {
  $('#username').focus();
});
