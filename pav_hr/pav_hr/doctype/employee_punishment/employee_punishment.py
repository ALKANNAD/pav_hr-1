# -*- coding: utf-8 -*-
# Copyright (c) 2021, Farouk Muharram and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint, _, scrub
from frappe.utils import get_url_to_form

class EmployeePunishment(Document):
	# def on_cancel(self):
	# 	emp_punshment = frappe.db.sql("""SELECT last_punishment_level, name FROM `tabEmployee Punishment`
    #  		WHERE last_punishment_level > %s
	# 		GROUP BY employee, type""", tuple([self.employee , self.last_punishment_level]), as_dict=True)
	# 	if emp_punshment:
	# 		frappe.throw(_("There is Employee Punishment Level > "))			
	# 	self.db_set("status", "Cancelled")

	def on_submit(self):
		if self.status not in ("Approved","Rejected"):
			frappe.throw(_("Only Employee Punishment with status 'Approved' and 'Rejected' can be submitted"))

	def validate(self):
		emp_punshment = frappe.db.sql("""SELECT employee_name, type, name FROM `tabEmployee Punishment`
     		WHERE employee=%s and type =%s and docstatus = 0 and name != %s
			GROUP BY employee, type""", tuple([self.employee , self.type, self.name]), as_dict=True)

		emp_punshment1 = frappe.db.sql("""SELECT employee_name, type, name FROM `tabEmployee Punishment`
     		WHERE employee=%s and type =%s and date = %s and name != %s
			GROUP BY employee, type""", tuple([self.employee, self.type, self.date, self.name]), as_dict=True)
		
		if emp_punshment:
			frappe.throw(_( "There is draft Employee Punshment with same employye %s and type %s need to be saved first %s"  
			% (self.employee_name, self.type, emp_punshment[0].name)))
		elif emp_punshment1:
			frappe.throw(_( "You cannot add more than one punshment on the same date for the same employee "))

	def fill_punishment_type(self):
		if not self.type:
			return
		last_punishment = frappe.db.sql("""SELECT a.name, a.employee, a.type, a.punishment_level FROM `tabEmployee Punishment` a 
		INNER JOIN 
		( SELECT name, employee, type, MAX(punishment_level) AS punishment_level FROM `tabEmployee Punishment` 
		WHERE
		 employee=%s and type =%s and docstatus = 1 and status='Approved' GROUP BY employee, type ) b 
		 ON a.employee = b.employee and a.type = b.type and a.punishment_level = b.punishment_level""", 
			 tuple([self.employee , self.type]), as_dict=True)
		last_level = 0
		last_punishment_name = None
		if last_punishment:
			last_punishment_name = last_punishment[0].name
			if last_punishment[0].punishment_level:
				last_level = int(last_punishment[0].punishment_level) 


		punishment_type = frappe.get_doc('Employee Punishment Type', self.type)

		if punishment_type :
			grade = {}
			if self.without_level == 0:
				grades = frappe.db.sql("""SELECT * FROM `tabPunishment Type Details` WHERE parent=%s""",
				 tuple([punishment_type.name]), as_dict=True)
				for g in grades:
					last = last_level + 1
					if int(g.punishment_level) == (last):
						grade = g
						break
				
				if not grade and grades:
					grade = max(grades, key=lambda item: item.punishment_level)
			else:
				grade = {
					'punishment_type' : punishment_type.punishment_type,
					'deduction' : punishment_type.deduction,
					'procedure' : punishment_type.procedure,
					}
			grade['last_punishment_level'] = last_level
			grade['is_editable'] = punishment_type.is_editable
			grade['employee_punishment'] = last_punishment_name

		return grade

	
@frappe.whitelist()
def get_emp_punshment(source_name):
	dic = frappe.db.sql("""SELECT date, type, punishment_type, punishment_level, deduction, `procedure` 
	FROM `tabEmployee Punishment` WHERE employee=%s and docstatus = 1 and status='Approved'""", tuple([source_name]), as_dict=True)
	
	for d in dic:
		if d['punishment_type'] == "Deduction":
			d['procedure'] = str(d['deduction'])
	return dic

@frappe.whitelist()
def get_emp_max_punshment(source_name):
	dic = frappe.db.sql(""" SELECT a.date, a.type, a.punishment_type, a.punishment_level, a.deduction, a.`procedure`, a.punishment_level
	 FROM `tabEmployee Punishment` a
	 INNER JOIN 
	(SELECT date, type, punishment_type, punishment_level, deduction, `procedure`, MAX(punishment_level) 
	as punishment_level FROM `tabEmployee Punishment` WHERE employee=%s and docstatus = 1 and status='Approved' GROUP BY type) b 
	ON a.type = b.type and a.punishment_level = b.punishment_level""",
	 tuple([source_name]), as_dict=True)
	 
	for d in dic:
		if d['punishment_type'] == "Deduction":
			d['procedure'] = str(d['deduction'])
	return dic