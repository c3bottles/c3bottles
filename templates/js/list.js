{% include "js/base.js" %}

{% import "macros/states.html" as states %}
{{ states.label_js() }}

list.initializeTable(mapSource);

var hash = location.hash.substr(1);
if (hash.length > 0) {
  var category = parseInt(hash);
  if (Number.isInteger(category)) {
    list.setCategory(category);
  }
}
