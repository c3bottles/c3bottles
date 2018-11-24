const $ = require('jquery');

$('.admin-button-user-delete').on('click', ev => {
  const link = $('#admin-link-user-delete');

  link.attr('href', `${link.data('href')}${$(ev.currentTarget).data('uid')}`);
  $('#admin-modal-user-delete').modal('show');
});
