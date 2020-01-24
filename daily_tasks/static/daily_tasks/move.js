function ShowHide(id) {
  var x = document.getElementById(id);
  if (x.style.display == 'none') {
    x.style.display = 'block';
  }
  else {
    x.style.display = 'none';
  }
};


var  search = document.getElementById('search_label');
var  filter = document.getElementById('filter_label');
search.style.cursor = 'pointer';
filter.style.cursor = 'pointer';
search.onclick = function() {ShowHide('search_content')};
filter.onclick = function() {ShowHide('filter_content')}
