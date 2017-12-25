const $ = require('jquery');
const offset = $("meta[name='time']").attr('content') - Date.now() / 1000;

require('datatables-bootstrap3-plugin');

const icon_details = $('<span></span>').addClass('clickable glyphicon glyphicon-search dp_modal details');
const icon_report = $('<span></span>').addClass('clickable glyphicon glyphicon-bullhorn dp_modal report');
const icon_visit = $('<span></span>').addClass('clickable glyphicon glyphicon-wrench dp_modal visit');

function get_table_data() {
  const arr = [];

  for (const num in drop_points) {
    if (!drop_points[num].removed) {
      arr.push(drop_points[num]);
    }
  }

  return arr;
}

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
    data: get_table_data(),
    order: [[6, 'desc']],
    createdRow(row, data) {
      drop_points[data.number].row = row;
    },
    columns: [
      {
        data: 'number',
      },
      {
        data: null,
        render(data) {
          if (data.description) {
            return data.description;
          }

          return `somewhere on level ${data.level}`;
        },
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
