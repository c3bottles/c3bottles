const $ = require('jquery');
const gettext = require('./gettext.js');

require('datatables.net-bs')(window, $);

const offset = $("meta[name='time']").attr('content') - Date.now() / 1000;

const icon_details = $('<span></span>').addClass('clickable glyphicon glyphicon-search dp_modal details');
const icon_report = $('<span></span>').addClass('clickable glyphicon glyphicon-bullhorn dp_modal report');
const icon_visit = $('<span></span>').addClass('clickable glyphicon glyphicon-wrench dp_modal visit');

let category = -1;

function get_table_data() {
  const arr = [];

  for (const num in drop_points) {
    if (!drop_points[num].removed && (category < 0 || drop_points[num].category_id === category)) {
      arr.push(drop_points[num]);
    }
  }

  return arr;
}

function setCategory(num) {
  category = num;
  $('.list-category-select-button')
    .removeClass('btn-primary')
    .addClass('btn-default');
  $('.list-category-select-button')
    .filter(`[data-category_id='${num}']`)
    .removeClass('btn-default')
    .addClass('btn-primary');
  dt.clear();
  dt.rows.add(get_table_data());
  dt.draw(true);
}

global.setListCategory = setCategory;

function redraw_table() {
  dt
    .rows()
    .invalidate()
    .draw(false);
  setTimeout(() => {
    redraw_table();
  }, 10000);
}

global.dt = undefined;
global.init_table = function() {
  dt = $('#dp_list').DataTable({
    language: gettext('dt'),
    paging: false,
    data: get_table_data(),
    order: [[5, 'desc']],
    createdRow(row, data) {
      drop_points[data.number].row = row;
    },
    columns: [
      {
        data: 'number',
      },
      {
        data: 'category',
      },
      {
        data: 'description_with_level',
      },
      {
        data: 'level',
      },
      {
        data: null,
        render(data, type) {
          if (type === 'sort') {
            return labels[data.last_state][0];
          }

          return labels[data.last_state][1][0].outerHTML;
        },
      },
      {
        data: null,
        sort: 'desc',
        className: 'hidden-xs',
        render(data) {
          const prio = (Date.now() / 1000 + offset - data.base_time) * data.priority_factor;

          drop_points[data.number].priority = prio.toFixed(2);

          return prio.toFixed(2);
        },
      },
      {
        data: 'reports_new',
        className: 'hidden-xs',
      },
      {
        data: null,
        orderable: false,
        defaultContent: '',
        createdCell(td, cd, rd) {
          rd.details_cell = td;
        },
        render(data) {
          const my_icon = icon_details.clone();

          my_icon.click(() => {
            show_dp_modal(data.number, 'details');
          });
          $(data.details_cell)
            .empty()
            .append(my_icon);
        },
      },
      {
        data: null,
        orderable: false,
        defaultContent: '',
        createdCell(td, cd, rd) {
          rd.report_cell = td;
        },
        render(data) {
          const my_icon = icon_report.clone();

          my_icon.click(() => {
            show_dp_modal(data.number, 'report');
          });
          $(data.report_cell)
            .empty()
            .append(my_icon);
        },
      },
      {
        data: null,
        orderable: false,
        defaultContent: '',
        createdCell(td, cd, rd) {
          rd.visit_cell = td;
        },
        render(data) {
          const my_icon = icon_visit.clone();

          my_icon.click(() => {
            show_dp_modal(data.number, 'visit');
          });
          $(data.visit_cell)
            .empty()
            .append(my_icon);
        },
      },
    ],
  });

  setTimeout(() => {
    redraw_table();
  }, 10000);
};

global.draw_row = function(num) {
  if (drop_points[num] && drop_points[num].row) {
    dt
      .row(drop_points[num].row)
      .data(drop_points[num])
      .draw(false);
  } else if (drop_points[num]) {
    dt.row.add(drop_points[num]).draw(false);
  }
};

$('.list-category-select-button').on('click', ev => {
  const num = $(ev.currentTarget).data('category_id');

  if (num > -1) {
    location.hash = `#${num}`;
  } else {
    location.hash = '';
  }
  setCategory(num);
});
