# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe.utils import add_months, nowdate

from erpnext.selling.doctype.sales_order.sales_order import make_material_request
from erpnext.selling.doctype.sales_order.test_sales_order import make_sales_order
from erpnext.selling.report.pending_so_items_for_purchase_request.pending_so_items_for_purchase_request import (
	execute,
)
from erpnext.tests.utils import ERPNextTestCase


class TestPendingSOItemsForPurchaseRequest(ERPNextTestCase):
    def test_result_for_partial_material_request(self):
        frappe.db.commit()
        frappe.db.begin()
        frappe.db.sql("""delete from `tabPurchase Invoice`
		where company in ('_Test Company', '_Test Company 1', '_Test Company with perpetual inventory')""")
        frappe.db.sql("""delete from `tabSales Order`""")
        frappe.db.sql("""delete from `tabSales Order Item`""")
        so = make_sales_order()
        mr=make_material_request(so.name)
        mr.items[0].qty = 4
        mr.schedule_date = add_months(nowdate(),1)
        mr.submit()
        report = execute()
        l = len(report[1])
        self.assertEqual((so.items[0].qty - mr.items[0].qty), report[1][l-1]['pending_qty'])
        frappe.db.rollback()

    def test_result_for_so_item(self):
        frappe.db.commit()
        frappe.db.begin()
        frappe.db.sql("""delete from `tabPurchase Invoice`
		where company in ('_Test Company', '_Test Company 1', '_Test Company with perpetual inventory')""")
        frappe.db.sql("""delete from `tabSales Order`""")
        frappe.db.sql("""delete from `tabSales Order Item`""")
        so = make_sales_order()
        report = execute()
        l = len(report[1])
        self.assertEqual(so.items[0].qty, report[1][l-1]['pending_qty'])
        frappe.db.rollback()
