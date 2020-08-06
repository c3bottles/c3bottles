const $ = require('jquery');

const token_renew_interval = 200 * $('meta[name="endpoint"]').data('token-interval');
const token = $('meta[name=csrf_token]').attr('content');
const api_url = $('meta[name="endpoint"]').data('api');

function setCSRFToken(token) {
    $.ajaxSetup({
      beforeSend(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', token);
        }
      },
    });
}

setCSRFToken(token);

setInterval(() => {
    $.get(`${api_url}token`).then(response => {
        setCSRFToken(response.token);
        $('input[name=csrf_token]').attr('value', response.token);
        $('meta[name=csrf_token]').attr('content', response.token);
    });
}, token_renew_interval);
