require('../common/main');
require('../common/csrf');

switch ($('meta[name=endpoint]').attr('content')) {
  case 'admin.index':
    require('../common/admin');
    break;
  case 'manage.create':
    global.map = require('../common/map');
    global.create = require('../common/create');
    require('../common/refresh');
    break;
  case 'manage.edit':
    global.map = require('../common/map');
    global.create = require('../common/create');
    require('../common/refresh');
    break;
  case 'view.details':
    require('../view/details');
    require('../common/refresh');
    break;
  case 'view.list_':
    require('../view/list');
    require('../common/refresh');
    break;
  case 'view.map_':
    require('../view/map');
    require('../common/refresh');
    break;
}
