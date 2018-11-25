const $ = require('jquery');

$('.admin-button-user-delete').on('click', ev => {
  $('#admin-input-user-delete-user-id').val($(ev.currentTarget).data('uid'));
  $('#admin-modal-user-delete').modal('show');
});
