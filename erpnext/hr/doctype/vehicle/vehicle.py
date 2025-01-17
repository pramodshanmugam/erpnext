# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class Vehicle(Document):
	def validate(self):
		if getdate(self.start_date) > getdate(self.end_date):
			frappe.throw(_("Insurance Start date should be less than Insurance End date"))
		if getdate(self.carbon_check_date) > getdate():
			frappe.throw(_("Last carbon check date cannot be a future date"))

def get_timeline_data(doctype, name):
	'''Return timeline for vehicle log'''
	return dict(frappe.db.multisql({
		'mariadb': '''select unix_timestamp(date), count(*)
	from `tabVehicle Log` where license_plate=%s
	and date > date_sub(CURRENT_DATE, interval 1 year)
	group by date''',
	'postgres': '''select extract(epoch from date), count(*)
	from `tabVehicle Log` where license_plate=%s
	and date > (current_date - 'interval 1 year')
	group by date''',
	}, name))
