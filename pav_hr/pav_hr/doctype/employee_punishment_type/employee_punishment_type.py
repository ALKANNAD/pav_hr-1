# -*- coding: utf-8 -*-
# Copyright (c) 2021, Farouk Muharram and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint, _

class EmployeePunishmentType(Document):
	def validate(self):
		if self.without_level == 1:			
			if self.punishment_type == "Procedure":
				if self.procedure == None:
					frappe.throw(_( "Please, fill procedure field"))				
			else:
				if self.deduction == None:
					frappe.throw(_( "Please, fill deduction fields"))

			self.punishment_details = None
		else:
			for t in self.punishment_details:
				if t.punishment_type == "Procedure":
					if t.procedure == None:
						frappe.throw(_( "Please, fill procedure fields"))				
				else:
					if t.deduction == None:
						frappe.throw(_( "Please, fill deduction fields"))
			self.punishment_type = None
			self.deduction = None
			self.procedure = None