function ShowHide(id) {
  var x = document.getElementById(id);
  if (x.style.display == 'none') {
    x.style.display = 'block';
  }
  else {
    x.style.display = 'none';
  }
};

function Show(id) {
  var x = document.getElementById(id);
  x.style.display = 'block';
  x.style.marginTop = '3%';

};

function Hide(id) {
  var x = document.getElementById(id);
  x.style.display = 'none';
};


var  ID = document.getElementById('ID');
var  KKS = document.getElementById('KKS');
var  NAME = document.getElementById('Name');
var  TYPE = document.getElementById('Type');
var  BLOCK = document.getElementById('Block');
var  STATUS = document.getElementById('Status');
var  UPDATED = document.getElementById('Updated');
var  CURR_STATUS = document.getElementById('Curr_status');

ID.style.cursor = 'pointer';
KKS.style.cursor = 'pointer';
NAME.style.cursor = 'pointer';
TYPE.style.cursor = 'pointer';
BLOCK.style.cursor = 'pointer';
STATUS.style.cursor = 'pointer';
UPDATED.style.cursor = 'pointer';
CURR_STATUS.style.cursor = 'pointer';

ID.onmouseover = function() {Show('tail_id', 'ID')};
ID.onmouseout = function() {Hide('tail_id', 'ID')};
KKS.onmouseover = function() {Show('tail_kks')};
KKS.onmouseout = function() {Hide('tail_kks')};
NAME.onmouseover = function() {Show('tail_name')};
NAME.onmouseout = function() {Hide('tail_name')};
TYPE.onmouseover = function() {Show('tail_type')};
TYPE.onmouseout = function() {Hide('tail_type')};
BLOCK.onmouseover = function() {Show('tail_block')};
BLOCK.onmouseout = function() {Hide('tail_block')};
STATUS.onmouseover = function() {Show('tail_status')};
STATUS.onmouseout = function() {Hide('tail_status')};
UPDATED.onmouseover = function() {Show('tail_updated')};
UPDATED.onmouseout = function() {Hide('tail_updated')};
CURR_STATUS.onmouseover = function() {Show('tail_curr_status')};
CURR_STATUS.onmouseout = function() {Hide('tail_curr_status')};