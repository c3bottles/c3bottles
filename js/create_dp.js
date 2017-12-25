const $ = require('jquery');
const L = require('leaflet');

require('./map.js');
const areas = require('./areas.js');
const gettext = require('./gettext.js');

let new_dp_marker = null;

function get_marker(latlng) {
  const marker = L.marker(latlng, {
    icon: get_icon('CREATED'),
    draggable: true,
  });

  $(map).one('zoomend', () => {
    if (map.hasLayer(marker)) {
      map.removeLayer(marker);
      get_marker(marker._latlng);
    }
  });
  marker.on('drag', function() {
    set_info_from_marker(this._latlng);
  });
  map.addLayer(marker);

  return marker;
}

global.draw_new_dp = function(lat, lng) {
  const latlng = L.latLng(lat, lng);

  new_dp_marker = get_marker(latlng);
  map.setView(new_dp_marker._latlng, 5);
};

global.set_info_from_marker = function(latlng) {
  const lat = latlng.lat.toFixed(2);
  const lng = latlng.lng.toFixed(2);

  $('#lat').val(lat);
  $('#lng').val(lng);
  const room = areas.get_room([lng, lat]);

  if (room !== null) {
    $('#description').val(room.name);
    $('#number').val(get_next_free_dp_num());
    $(`input[name='level'][value=${room.level}]`).prop('checked', true);
  } else {
    const level = areas.get_level([lng, lat]);

    if (level !== null) {
      $('#number').val(get_next_free_dp_num());
      $(`input[name='level'][value=${level}]`).prop('checked', true);
    }
  }
};

global.init_dp_creation = function() {
  map.on('click', e => {
    if (!new_dp_marker) {
      const latlng = e.latlng;

      new_dp_marker = get_marker(latlng);
      set_info_from_marker(latlng);
    }
  });
};

$('.btn-number').click(function() {
  const field = $(this).data('field');
  const type = $(this).data('type');
  const input = $(`input[name='${field}']`);
  const val = Number.parseInt(input.val(), 10);

  if (!isNaN(val)) {
    if (type === 'minus') {
      if (val > input.attr('min')) {
        input.val(val - 1).change();
      }
      // eslint-disable-next-line
      if (Number.parseInt(input.val(), 10) == input.attr('min')) {
        $(this).attr('disabled', true);
      }
    } else if (type === 'plus') {
      if (val < input.attr('max')) {
        input.val(val + 1).change();
      }
      // eslint-disable-next-line
      if (Number.parseInt(input.val(), 10) == input.attr('max')) {
        $(this).attr('disabled', true);
      }
    }
  } else {
    input.val(0);
  }
});

$('.input-number').focusin(function() {
  $(this).data('old', $(this).val());
});

$('.input-number').change(function() {
  const min = Number.parseInt($(this).attr('min'), 10);
  const max = Number.parseInt($(this).attr('max'), 10);
  const val = Number.parseInt($(this).val(), 10);
  const name = $(this).attr('name');

  if (val >= min) {
    $(`.btn-number[data-type='minus'][data-field='${name}']`).removeAttr('disabled');
  } else {
    alert(gettext('Sorry, the minimum value was reached.'));
    $(this).val($(this).data('old'));
  }
  if (val <= max) {
    $(`.btn-number[data-type='plus'][data-field='${name}']`).removeAttr('disabled');
  } else {
    alert(gettext('Sorry, the maximum value was reached.'));
    $(this).val($(this).data('old'));
  }
});

$('.input-number').keydown(e => {
  // Allow: backspace, delete, tab, escape, enter and .
  if (
    $.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
    // Allow: Ctrl+A
    (e.keyCode === 65 && e.ctrlKey === true) ||
    // Allow: home, end, left, right
    (e.keyCode >= 35 && e.keyCode <= 39)
  ) {
    // let it happen, don't do anything
    return;
  }
  // Ensure that it is a number and stop the keypress
  if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
    e.preventDefault();
  }
});
