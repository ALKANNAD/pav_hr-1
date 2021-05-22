// Copyright (c) 2021, Farouk Muharram and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Punishment Type', {
	refresh(frm) {
		cur_frm.cscript.gradeTalbe(frm);
	},

	without_level(frm) {
		cur_frm.cscript.gradeTalbe(frm);
	},
});

frappe.ui.form.on("Punishment Type Details", {

	punishment_type:function(frm, cdt, cdn){
	var u = locals[cdt][cdn];
	if(u['punishment_type'] == "Procedure"){
		u['deduction'] = null;
		frm.refresh_field("deduction");
	}else{
		u['procedure'] = null;
		frm.refresh_field("procedure");
	}
	  }
  });
  
cur_frm.cscript.gradeTalbe = function(frm){
	if(frm.doc.without_level == 1){
		frm.set_df_property("punishment_details", "reqd", 0);
		frm.set_df_property("punishment_type", "reqd", 1);
	}else{
		frm.set_df_property("punishment_details", "reqd", 1);
		frm.set_df_property("punishment_type", "reqd", 0);
	}
}