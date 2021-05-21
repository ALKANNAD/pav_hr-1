# -*- coding: utf-8 -*-
# Copyright (c) 2021, Farouk Muharram and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint, _, scrub
from frappe.utils import get_url_to_form

class EmployeePunishment(Document):
	def validate_duplcate(self):
		emp_punshment = frappe.db.sql("""SELECT employee_name, type, name FROM `tabEmployee Punishment`
     		WHERE employee=%s and type =%s and docstatus = 0 and name != %s
			 GROUP BY employee, type""", tuple([self.employee , self.type, self.name]), as_dict=True)
		
		if emp_punshment:
			return emp_punshment[0]


	def fill_punishment_type(self):
		if not self.type:
			return
		emp_level = frappe.db.sql("""SELECT employee, type, MAX(last_punishment_level) as level FROM `tabEmployee Punishment`
     		WHERE employee=%s and type =%s and docstatus = 1 GROUP BY employee, type""", tuple([self.employee , self.type]), as_dict=True)
		last_level = 0
		if emp_level and len(emp_level) > 0:
			last_level = int(emp_level[0].level)
		if emp_level:
			last_level =  last_level + 1	
		cur_level =  last_level + 1

		punishment_type = frappe.get_doc('Employee Punishment Type', self.type)

		if punishment_type :
			grade = {}
			if self.without_level == 0:
				grades = frappe.db.sql("""SELECT * FROM `tabPunishment Type Details` WHERE parent=%s""",
				 tuple([punishment_type.name]), as_dict=True)
				for g in grades:
					if int(g.punishment_level) == cur_level:
						grade = g
				
				if not grade and grades:
					grade = max(grades, key=lambda item: item.punishment_level)
				grade['last_punishment_level'] = last_level
			else:
				grade = {
					'last_punishment_level' : last_level,
					'punishment_type' : punishment_type.punishment_type,
					'deduction' : punishment_type.deduction,
					'procedure' : punishment_type.procedure,
					}

		return grade

	
@frappe.whitelist()
def get_emp_punshment(source_name):
	dic = frappe.db.sql("""SELECT date, type, punishment_type, punishment_level, deduction, `procedure` 
	FROM `tabEmployee Punishment` WHERE employee=%s and docstatus = 1""", tuple([source_name]), as_dict=True)
	
	for d in dic:
		if d['punishment_type'] == "Deduction":
			d['procedure'] = str(d['deduction'])
	return dic

@frappe.whitelist()
def get_emp_max_punshment(source_name):
	dic = frappe.db.sql("""SELECT date, type, punishment_type, punishment_level, deduction, `procedure`, MAX(punishment_level) as punishment_level 
	FROM `tabEmployee Punishment` WHERE employee=%s and docstatus = 1 GROUP BY type""", tuple([source_name]), as_dict=True)
	 
	for d in dic:
		if d['punishment_type'] == "Deduction":
			d['procedure'] = str(d['deduction'])
	return dic