<%def name="header()">
% if tmpl_context.menu_widget:
<div id="moksha_menu" style="display:none;">
  <center> ${tmpl_context.menu_widget.display()|n} </center>
</div>
% endif
</%def>
