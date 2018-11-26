{% import "macros/states.html" as states %}
{% include "js/dp.js" %}
{{ states.label_js() }}
init_table();
var hash = location.hash.substr(1);
if (hash.length > 0) {
  var category = parseInt(hash);
  if (Number.isInteger(category)) {
    setListCategory(category);
  }
}
