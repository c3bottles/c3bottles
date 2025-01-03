const $ = require('jquery');
const gettext = require('./gettext.js');

const offset = $('meta[name="time"]').attr('content') - Date.now() / 1000;
const api_url = $('meta[name="endpoint"]').data('api');

function add_alert(type, title, message) {
  const alert = $('<div></div>')
    .addClass(`alert alert-${type} collapse`)
    .html(
      `${'<button type="button" class="close alert-hide">' +
        '<span aria-hidden="true">&times;</span></button>' +
        '<strong>'}${title}</strong> ${message}`
    );

  $('#alerts').prepend(alert);
  $('.alert-hide').on('click', e => {
    $(e.currentTarget)
      .parent()
      .slideUp();
  });
  alert.slideDown();
  setTimeout(() => {
    alert.slideUp();
  }, 5000);
}

function report_dp(num, state) {
  $('#dp_modal').modal('hide');
  $.ajax({
    type: 'POST',
    url: `${api_url}report`,
    data: {
      number: num,
      state,
    },
    dataType: 'json',
    success(response) {
      add_alert('success', gettext('Thank you!'), gettext('Your report has been received successfully.'));
      $.extend(true, drop_points, response);
      if (typeof(global.refreshDropPoint) === 'function') {
        global.refreshDropPoint(num);
      }
    },
    error(response) {
      const errors = $.parseJSON(response.responseText);

      for (const i in errors) {
        for (const key in errors[i]) {
          add_alert(
            'danger',
            gettext('Oh no!'),
            gettext('An error occurred while processing your report: ') + errors[i][key]
          );
        }
      }
    },
  });
}

$('#dp_modal').on('hidden.bs.modal', e => {
  $(e.currentTarget).removeData('bs.modal');
});

$('.modal-body .report-button').each(function() {
  $(this).on('click', e => {
    report_dp(
      $('.modal_dp_number')
        .first()
        .text(),
      $(e.target).val()
    );
  });
});

function showPane(pane) {
  for (let arr = ['details', 'report', 'visit'], i = 0; i < arr.length; i++) {
    $(`#dp_modal_${arr[i]}_tab`).removeClass('active');
    $(`#dp_modal_${arr[i]}_link`).removeClass('active');
  }
  $(`#dp_modal_${pane}_tab`).addClass('active');
  $(`#dp_modal_${pane}_link`).addClass('active');
}

function visit_dp(num, action) {
  if (action === 'EMPTIED') {
    $('#dp_modal').modal('hide');
  } else {
    showPane('report');
  }
  $.ajax({
    type: 'POST',
    url: `${api_url}visit`,
    data: {
      number: num,
      maintenance: action,
    },
    dataType: 'json',
    success(response) {
      add_alert('success', gettext('Thank you!'), gettext('Your visit has been logged successfully.'));
      $.extend(true, drop_points, response);
      if (typeof(global.refreshDropPoint) === 'function') {
        global.refreshDropPoint(num);
      }
    },
    error(response) {
      const errors = $.parseJSON(response.responseText);

      for (const i in errors) {
        for (const key in errors[i]) {
          add_alert(
            'danger',
            gettext('Oh no!'),
            gettext('An error occurred while processing your visit: ') + errors[i][key]
          );
        }
      }
    },
  });
}

$('.visit-button').each(function() {
  $(this).on('click', e => {
    visit_dp(
      $('.modal_dp_number')
        .first()
        .text(),
      $(e.target).val()
    );
  });
});

module.exports.show = function(num, pane) {
  const prio = (Date.now() / 1000 + offset - drop_points[num].base_time) * drop_points[num].priority_factor;

  drop_points[num].priority = prio.toFixed(2);
  const details = drop_points[num];

  for (const key in details) {
    $(`.modal_dp_${key}`).text(details[key]);
  }
  $('.dp-label').prop('hidden', true);
  $(`.dp-label.${drop_points[num].last_state}`).prop('hidden', false);
  const links = $('.modal_dp_link');

  for (let i = 0; i < links.length; i++) {
    $(links[i]).attr('href', `${$(links[i]).data('baseurl')}/${num}`);
  }
  const maplink = $('.modal_map_link');

  $(maplink).attr(
    'href',
    `${$(maplink).data('baseurl')}#${drop_points[num].level}/${drop_points[num].lat}/${drop_points[num].lng}/4`
  );
  showPane(pane);
  $('#dp_modal').modal('show');
};
