import json
import frappe

def execute():
    if frappe.db.exists("Social Login Key", "github"):
        auth_url_data = json.dumps({"scope": "user:email public_repo"})

        frappe.db.set_value(
            "Social Login Key",
            "github",
            "auth_url_data",
            auth_url_data
        )

        frappe.clear_cache(doctype="Social Login Key")
