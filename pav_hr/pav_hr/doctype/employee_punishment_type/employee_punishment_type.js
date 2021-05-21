// Copyright (c) 2021, Farouk Muharram and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Punishment Type', {
	validate(frm){

		if(frm.doc.without_level == 1){
			frm.doc.punishment_details = null;
		}else{
			frm.doc.punishment_type = null;
			frm.doc.deduction = null;
			frm.doc.procedure = null;

			$.each(frm.doc.punishment_details || [], function(i, v) {
				if(v.punishment_type == "Procedure"){
					if(v.procedure == null){
						frappe.msgprint(__("Please, fill all req fields"));
        				frappe.validated = false;
					}						
				}else{
					if(v.deduction == null){
						frappe.msgprint(__("Please, fill all req fields"));
        				frappe.validated = false;
					}	
				}
					
			});
		}
	},
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
		frm.set_df_property("punishment_grade", "reqd", 0);
	}else{
		frm.set_df_property("punishment_grade", "reqd", 1);
	}
}