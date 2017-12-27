const $ = require('jquery');
const gettext = require('./gettext.js');
const offset = $("meta[name='time']").attr('content') - Date.now() / 1000;

function add_alert(type, title, message) {
  const alert = $('<div></div>')
    .addClass(`alert alert-${type} collapse`)
    .html(
      `${'<button type="button" class="close alert-hide">' +
        '<span aria-hidden="true">&times;</span></button>' +
        '<strong>'}${title}</strong> ${message}`
    );

  $('#alerts').prepend(alert);
  $('.alert-hide').on('click', function() {
    $(this)
      .parent()
      .slideUp();
  });
  alert.slideDown();
  setTimeout(() => {
    alert.slideUp();
  }, 5000);
}

/*
 * Report a drop point through the AJAX API.
 *
 * The state of the drop point in question is sent through the API and the
 * modal with the buttons is hidden. After the API request has been finished,
 * an alert indicating success or failure is displayed.
 *
 */
function report_dp(num, state) {
  $('#dp_modal').modal('hide');
  $.ajax({
    type: 'POST',
    url: apiurl,
    data: {
      action: 'report',
      number: num,
      state,
    },
    dataType: 'json',
    success(response) {
      add_alert('success', gettext('Thank you!'), gettext('Your report has been received successfully.'));
      $.extend(true, drop_points, response);
      refresh_drop_point(num);
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

/*
 * When hiding any of the drop point modals (details, reporting, visiting),
 * the modal must be destroyed to be re-constructed on the next show instead
 * of simply hiding it and displaying the same instance again.
 *
 */
$('#dp_modal').on('hidden.bs.modal', function() {
  $(this).removeData('bs.modal');
});

/*
 * Add an event handler to all the report buttons.
 *
 */
$('.report-button').each(function() {
  $(this).on('click', e => {
    report_dp(
      $('.modal_dp_number')
        .first()
        .text(),
      $(e.target).val()
    );
  });
});

/*
 * Select a specific given pane in the drop point modal.
 *
 */
function show_dp_modal_pane(pane) {
  for (let arr = ['details', 'report', 'visit'], i = 0; i < arr.length; i++) {
    $(`#dp_modal_${arr[i]}_tab`).removeClass('active');
    $(`#dp_modal_${arr[i]}_link`).removeClass('active');
  }
  $(`#dp_modal_${pane}_tab`).addClass('active');
  $(`#dp_modal_${pane}_link`).addClass('active');
}

/*
 * Log the visit of a drop point through the AJAX API.
 *
 * The action performed when visiting the drop point is sent through the API
 * and the modal with the buttons is hidden. After the API request has been
 * finished, an alert indicating success or failure is displayed.
 *
 */
function visit_dp(num, action) {
  if (action === 'EMPTIED') {
    $('#dp_modal').modal('hide');
  } else {
    show_dp_modal_pane('report');
  }
  $.ajax({
    type: 'POST',
    url: apiurl,
    data: {
      action: 'visit',
      number: num,
      maintenance: action,
    },
    dataType: 'json',
    success(response) {
      add_alert('success', gettext('Thank you!'), gettext('Your visit has been logged successfully.'));
      $.extend(true, drop_points, response);
      refresh_drop_point(num);
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

/*
 * Add an event handler to all the visit buttons.
 */
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

/*
 * When showing any pane of the drop point modal (details, reporting,
 * visiting), all elements displaying details of the drop point in question are
 * filled with the correct details before the modal is made visible to the user.
 * All the details are read from the drop point JSON object.
 *
 * In addition, the correct pane of the modal is selected and the modal is
 * shown.
 *
 */
global.show_dp_modal = function(num, pane) {
  const prio = (Date.now() / 1000 + offset - drop_points[num].base_time) * drop_points[num].priority_factor;

  drop_points[num].priority = prio.toFixed(2);
  const details = drop_points[num];

  for (const key in details) {
    $(`.modal_dp_${key}`).text(details[key]);
  }
  if (details.type === 'trashcan') {
    $('.modal_dp-title').text(gettext('Trashcan'));
    $('#dp_modal_report_link').hide();
    $('#dp_modal_visit_link').hide();
    // eslint-disable-next-line
    pane = 'details';
  } else {
    $('.modal_dp-title').text(gettext('Drop Point'));
    $('#dp_modal_report_link').show();
    $('#dp_modal_visit_link').show();
  }
  const links = $('.modal_dp_link');

  for (let i = 0; i < links.length; i++) {
    $(links[i]).attr('href', `${$(links[i]).data('baseurl')}/${num}`);
  }
  const maplink = $('.modal_map_link');

  $(maplink).attr('href', `${$(maplink).data('baseurl')}#${drop_points[num].lat}/${drop_points[num].lng}/4`);
  show_dp_modal_pane(pane);
  $('#dp_modal').modal('show');
};
