$('body').on('click', 'a[data-toggle=collapse]', function() {
	var _self = $(this);
	var _group = _self.parent().parent().parent();
	var _button = _group.children('button');
	var _target = $(_self.attr('data-target'));
	if (_target.hasClass('in')) {
		_self.parent().removeClass('active');
	} else {
		_self.parent().addClass('active');
	}
	if (_group.find("li.active").length > 0) {
		_button.removeClass("btn-default").addClass("btn-primary");
	} else {
		_button.removeClass("btn-primary").addClass("btn-default");
	}
});
