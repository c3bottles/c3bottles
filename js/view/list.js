const list = require('../common/list');

global.drop_points = $.parseJSON($('meta[name=all-drop-points]').attr('content'));

list.initializeTable();

const hash = location.hash.substr(1);
if (hash.length > 0) {
  var category = parseInt(hash);
  if (Number.isInteger(category)) {
    list.setCategory(category);
  }
}
