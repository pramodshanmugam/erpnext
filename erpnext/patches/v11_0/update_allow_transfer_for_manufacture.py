# Copyright (c) 2018, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import frappe


def execute():
	frappe.reload_doc('stock', 'doctype', 'item')
	frappe.db.sql(""" update `tabItem` set include_item_in_manufacturing = 1
		where coalesce(is_stock_item, 0) = 1""")

	for doctype in ['BOM Item', 'Work Order Item', 'BOM Explosion Item']:
		frappe.reload_doc('manufacturing', 'doctype', frappe.scrub(doctype))

		frappe.db.sql(""" update `tab{0}` child, tabItem item
			set
				child.include_item_in_manufacturing = 1
			where
				child.item_code = item.name and coalesce(item.is_stock_item, 0) = 1
		""".format(doctype))
