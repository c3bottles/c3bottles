const $ = require('jquery');

$('.admin-button-user-delete').on('click', ev => {
  $('#admin-input-user-delete-user-id').val($(ev.currentTarget).data('uid'));
  $('#admin-modal-user-delete').modal('show');
});

$('.admin-button-user-enable').on('click', ev => {
  $('#admin-input-user-enable-user-id').val($(ev.currentTarget).data('uid'));
  $('#admin-form-user-enable').submit();
});

$('.admin-button-user-disable').on('click', ev => {
  $('#admin-input-user-disable-user-id').val($(ev.currentTarget).data('uid'));
  $('#admin-form-user-disable').submit();
});
