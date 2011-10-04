var overlay_selector = '#pb_9991';
var overlay_content_selector = overlay_selector + ' .pb-ajax';
var content_selector = overlay_content_selector;

jq('body').append('<div id="pb_9991" class="overlay overlay-ajax "><div class="close"><span>Close</span></div><div class="pb-ajax"></div></div>');

$("#pb_9991").overlay({
    onClose : function(){
        $(overlay_content_selector).html('');//clear it
    }
});

function getOverlayConfig(){
  var context_input = jq('input[name="form.widgets.context:list"]:checked');
  return { 
    manager : jq("#form-widgets-manager").val(), 
    context : context_input.val(),
    context_ele : context_input.closest('span.option').clone(),
    portlet : jq('#form-widgets-portlet').val()
  }
}

function portletHash(){
  return jq("#form-widgets-manager").val() + '-' + 
    jq('#form-widgets-portlet').val() + '-' +
    jq('input[name="form.widgets.context:list"]:checked').val()
}

function decodeHash(hash){
  var split = hash.split('-', 2);
  var rest = hash.split('-');
  return {
    manager : split[0].replace(' ', ''),
    portlet : split[1].replace(' ', ''),
    context : rest.slice(2).join('-')
  }
}

function loadOverlay(selected){
  var qs = '';
  var manager = false;
  var context = false;
  var portlet = false;
  
  ed = tinyMCE.activeEditor;
  if(ed == null){
    return;
  }
  item = ed.selection.getNode();
  jqitem = jq(item);

  isCurrentPortlet = function(){
    return (jqitem.length > 0 && jqitem.hasClass('mce-only'));
  }
  
  if(isCurrentPortlet() && selected == undefined){
    var hash = jqitem[0].className.replace('mce-only', '').replace('TINYMCEPORTLET', '').replace(' ', '')
    selected = decodeHash(hash);
  }
  
  if(selected != undefined){
    qs = '?';
    manager = selected.manager
    qs += 'manager=' + manager;
    context = selected.context
    qs += '&context=' + context;
    portlet = selected.portlet;
    qs += '&portlet=' + portlet
  }
  
  
  var wrap = $(overlay_content_selector);
  var url = $('base').attr('href') + '/@@add-tinymce-portlet' + qs;
  jq.ajax({
    url : url, 
    success: function(data, textStatus, req){
      wrap.html(data);


      if(isCurrentPortlet()){
      
      }else{
        jq(content_selector + ' input[name="form.buttons.save"]').attr('value', 'Add');
        jq(content_selector + ' input[name="form.buttons.remove"]').hide();
      }
      if(manager != false){
        jq(content_selector + ' #form-widgets-manager').val(manager);
      }
      if(context != false){
        var input = jq(content_selector + ' input[value="' + context + '"]');
        if(input.length > 0){
          input[0].checked = true;
        }else{
          if(selected.context_ele != undefined && selected.context_ele.length > 0){
            input = selected.context_ele;
            input.find('input')[0].checked = true;
            jq('#form-widgets-context-input-fields').append(input);
          }
        }
      }
      if(portlet != false){
        var input = jq('#form-widgets-portlet input[value="' + portlet + '"]');
        if(input.length > 0){
          input[0].checked = true;
        }else if(selected.context_ele == undefined){
          jq("#form-widgets-portlet").html('<option value="' + portlet + '" id="form-widgets-portlet-0">' + portlet + '</option>');
        }
      }
    }
  });
  $(overlay_selector).overlay().load();
}

jq(content_selector + ' input[name="form.buttons.save"]').live('click', function(){
  var node = tinyMCE.activeEditor.selection.getNode();
  var item = jq(node);
  if(item.length > 0 && item.hasClass('mce-only')){
    item[0].className = "TINYMCEPORTLET mce-only " + portletHash();
  }else{
    item.append('<img class="TINYMCEPORTLET mce-only ' + portletHash() + '" src="++resource++collective.tinymceportlets/add-portlets.png" />');
  }
  $(overlay_selector).overlay().close();
});

jq(content_selector + ' input[name="form.buttons.cancel"]').live('click', function(){
  $(overlay_selector).overlay().close();
  return false;
});

jq(content_selector + ' input[name="form.buttons.remove"]').live('click', function(){
  var node = tinyMCE.activeEditor.selection.getNode();
  var item = jq(node);
  item.remove();
  $(overlay_selector).overlay().close();
});

jq(content_selector + ' #form-widgets-manager,input[name="form.widgets.context:list"]').live('change', function(){
  loadOverlay(getOverlayConfig());
});

jq(content_selector + ' form#form').live('submit', function(){ return false; });

(function() {
  tinymce.create('tinymce.plugins.PortletsPlugin', {
    init : function(ed, url) {
      // Register the command so that it can be invoked by using tinyMCE.activeEditor.execCommand('mceExample');
	    ed.addCommand('mceportlets', function() {
		    try{
          loadOverlay();
		    }catch(e){
		      alert('Whoops. Something went wrong!');
		    }
      });

	    // Register example button
	    ed.addButton('mceportlets', {
		    title : 'Add/Edit portlet here.',
		    cmd : 'mceportlets',
		    image : url + '/add-portlets.png'
	    });
	  }
  });
  tinymce.PluginManager.add('mceportlets', tinymce.plugins.PortletsPlugin);
})();