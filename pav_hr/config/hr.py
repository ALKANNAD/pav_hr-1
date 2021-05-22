from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Punishment"),
			"items": [
				{
					"type": "doctype",
					"name": "Employee Punishment",
					"description":_("Employee Punishment"),
					"onboard": 1,
					"dependencies": ["Employee"],
				},
                {
					"type": "doctype",
					"name": "Employee Punishment Type",
					"description":_("Employee Punishment Type"),
					"onboard": 1,
					"dependencies": ["Employee"],
				},
			]
		},
	]