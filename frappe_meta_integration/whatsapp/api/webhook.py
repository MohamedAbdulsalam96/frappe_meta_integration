import frappe
from werkzeug.wrappers import Response
import string
import random

@frappe.whitelist(allow_guest=True)
def handle():
    if frappe.request.method == "GET":
        return verify_token_and_fulfill_challenge()

    try:
        form_dict = frappe.local.form_dict
        res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        frappe.get_doc(
            {"doctype": "Note", "title":res, "content": frappe.as_json(form_dict)}
        ).insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception:
        frappe.log_error("WhatsApp Webhook Log Error", frappe.get_traceback())
        frappe.throw("Something went wrong")

def verify_token_and_fulfill_challenge():
	meta_challenge = frappe.form_dict.get("hub.challenge")
	expected_token = frappe.db.get_single_value("WhatsApp Cloud API Settings", "webhook_verify_token")

	if frappe.form_dict.get("hub.verify_token") != expected_token:
		frappe.throw("Verify token does not match")

	return Response(meta_challenge, status=200)
