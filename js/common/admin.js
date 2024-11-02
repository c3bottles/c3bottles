const $ = require('jquery');

$('.admin-button-user-enable').on('click', ev => {
  $('#admin-input-user-enable-user-id').val($(ev.currentTarget).data('uid'));
  $('#admin-form-user-enable').submit();
});

$('.admin-button-user-disable').on('click', ev => {
  $('#admin-input-user-disable-user-id').val($(ev.currentTarget).data('uid'));
  $('#admin-form-user-disable').submit();
});

$('.admin-button-user-permissions').on('click', ev => {
  $('#admin-input-user-permissions-user-id').val($(ev.currentTarget).data('uid'));
  $('#admin-input-user-permissions-can-visit').prop('checked', $(ev.currentTarget).data('visit'));
  $('#admin-input-user-permissions-can-edit').prop('checked', $(ev.currentTarget).data('edit'));
  $('#admin-input-user-permissions-is-admin').prop('checked', $(ev.currentTarget).data('admin'));
  $('#admin-modal-user-permissions').modal('show');
});

$('.admin-button-user-password').on('click', ev => {
  $('#admin-input-user-password-user-id').val($(ev.currentTarget).data('uid'));
  $('#admin-modal-user-password').modal('show');
});

$('.admin-button-user-delete').on('click', ev => {
  $('#admin-input-user-delete-user-id').val($(ev.currentTarget).data('uid'));
  $('#admin-modal-user-delete').modal('show');
});

$('#admin-button-create-all-labels-pdf').on('click', ev => {
  $(ev.currentTarget)
    .attr('disabled', true)
    .prepend('<i class="fas fa-circle-notch fa-spin"></i> ');
});

$('#admin-button-create-all-labels-zip').on('click', ev => {
  $(ev.currentTarget)
    .attr('disabled', true)
    .prepend('<i class="fas fa-circle-notch fa-spin"></i> ');
});
