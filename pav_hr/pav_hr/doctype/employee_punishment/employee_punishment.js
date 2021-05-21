// Copyright (c) 2021, Farouk Muharram and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Punishment', {
	setup(frm) {
		frm.set_query('employee', () => {
            return {
				filters: {
					company: frm.doc.company
					 }
				};
            });
		},
	refresh(frm){
		frm.set_df_property("punishment_level", "read_only", 1);
	},
	validate(frm){
		frappe.call({
			method: "validate_duplcate",
			doc: frm.doc,
			callback: function(r) {
				if(r.message){
					frm.set_value('type', null);
					frappe.msgprint(__(`There is draft Employee Punshment with same employye ${r.message.employee_name} and type ${r.message.type} need to be saved first ${r.message.name}`));
					frappe.validated = false;
				}		
			}
		}); 

	},
	type(frm) {
		if(frm.doc.type == null){
			frm.set_value('punishment_level', null);
			frm.set_value('punishment_type', null);
			frm.set_value('deduction', null);
			frm.set_value('procedure', null);
			frm.set_value('last_punishment_level', null);
			return;
		}
		if(frm.doc.employee == null){
			frappe.msgprint(__("Please, Chose Employee First"));
		}
		frappe.call({
			method: "fill_punishment_type",
			doc: frm.doc,
			callback: function(r) {
				cur_frm.cscript.typeCallback(frm, r.message);
				
			}
		});  
	},
	employee(frm) {
		if(frm.doc.type == null)
					return;
		frappe.call({
			method: "fill_punishment_type",
			doc: frm.doc,
			callback: function(r) {
				cur_frm.cscript.typeCallback(frm, r.message);				
			}
		});  
	}
});

cur_frm.cscript.typeCallback = function(frm, message){
	console.log(message);
	if(message == null){
		frm.set_value('punishment_level', null);
		frm.set_value('punishment_type', null);
		frm.set_value('deduction', null);
		frm.set_value('procedure', null);
		frm.set_value('last_punishment_level', null);
		return;
	}

	if(frm.doc.without_level == 0)
		frm.set_value('punishment_level', message.punishment_level);
	else
		frm.set_value('punishment_level', null);

	frm.set_value('punishment_type', message.punishment_type);
	frm.set_value('procedure', message.procedure);
	frm.set_value('deduction', message.deduction);
	if(message.last_punishment_level == 0 )
		message.last_punishment_level = "0";
	frm.set_value('last_punishment_level', message.last_punishment_level);
}