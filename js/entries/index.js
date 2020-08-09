require('../common/main');
require('../common/csrf');

switch ($('meta[name=endpoint]').attr('content')) {
  case 'admin.index':
    require('../common/admin');
    break;
  case 'manage.create':
    require('../manage/create');
    break;
  case 'manage.edit':
    require('../manage/edit');
    break;
  case 'view.details':
    require('../view/details');
    break;
  case 'view.list_':
    require('../view/list');
    break;
  case 'view.map_':
    require('../view/map');
    break;
}
