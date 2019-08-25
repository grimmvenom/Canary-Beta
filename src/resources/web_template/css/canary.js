
// On Page Load refresh checkboxes and radio buttons
function UncheckAll(){
  var w = document.getElementsByTagName('input');
  for(var i = 0; i < w.length; i++){
    if (w[i].type=='text' || w[i].type=='password' || w[i].type=='file'){
      w[i].value = "";
    }
    if(w[i].type=='checkbox'){
      w[i].checked = false;
    }
    if(w[i].type=='radio'){
      w[i].checked = false;
    }
  }
  document.getElementById('url_text').value = '';
  document.getElementById('url_text').style.display = 'none';
  document.getElementById('url_file').value = '';
  document.getElementById('database').value = '';
  document.getElementById('limit_domain').value = '';
  document.getElementById('excel_enable').checked = false;
  document.getElementById('advanced_enable').checked = false;
  document.getElementById('execute_automation').checked = false;

}

window.onload = UncheckAll()

// URL Selection
function show_url_textarea(){
  document.getElementById('url-text-input').style.display = 'block';
  document.getElementById('url-file-input').style.display = 'none';
  document.getElementById('url_file').value = '';
}
function show_url_file(){
  document.getElementById('url-file-input').style.display = 'block';
  document.getElementById('url-text-input').style.display = 'none';
  document.getElementById('url_text').value = '';
}

function show_advanced_options(){
  if (document.getElementById('enhancers').style.display !== 'none') {
    document.getElementById('enhancers').style.display = 'none';
  }
  else {
    document.getElementById('enhancers').style.display = 'block';
  }

}
function show_base_url(){
  if (document.getElementById('base_url').style.display !== 'none') {
    document.getElementById('base_url').style.display = 'none';
  }
  else {
    document.getElementById('base_url').style.display = 'block';
  }
}
function show_domain_limit(){
  if (document.getElementById('limit_domain').style.display !== 'none') {
    document.getElementById('limit_domain').style.display = 'none';
  }
  else {
    document.getElementById('limit_domain').style.display = 'block';
  }
}
function show_exclude_domain(){
  if (document.getElementById('exclude_domain').style.display !== 'none') {
    document.getElementById('exclude_domain').style.display = 'none';
  }
  else {
    document.getElementById('exclude_domain').style.display = 'block';
  }
}
function show_authentication(){
  if (document.getElementById('authentication').style.display === 'none') {
    document.getElementById('authentication').style.display = 'block';
  }
  else {
    document.getElementById('authentication').style.display = 'none';

  }
}
function show7(){
  if (document.getElementById('database_info').style.display == 'none') {
    document.getElementById('database_info').style.display = 'block';
  }
  else {
    document.getElementById('database_info').style.display = 'none';
  }
}

