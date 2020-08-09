const list = require('../common/list');

global.drop_points = $.parseJSON($('meta[name=all-drop-points]').attr('content'));

list.initializeTable();

const hash = location.hash.substr(1);

if (hash.length > 0) {
  const category = parseInt(hash, 10);

  if (Number.isInteger(category)) {
    list.setCategory(category);
  }
}
