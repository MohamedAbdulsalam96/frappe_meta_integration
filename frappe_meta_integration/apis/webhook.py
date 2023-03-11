import frappe
import requests
import random

@frappe.whitelist(allow_guest=True)
def handle():
    if frappe.request.method == "GET":
        return verify_token_and_fulfill_challenge()

def verify_token_and_fulfill_challenge():
    note = frappe.new_doc("Note")
    ran = random.randint(0, 1000)
    note.title = "Webhook Testing - " + str(ran)
    note.content = frappe.form_dict.get("hub")
    mode = frappe.form_dict.get("hub.mode")
    token = frappe.form_dict.get("hub.verify_token")
    challenge = frappe.form_dict.get("hub.challenge")

    expected_token = frappe.db.get_single_value("WhatsApp Cloud API Settings", "webhook_verify_token")

    if (mode and token):
        if (mode == "subscribe" and token == expected_token):
            note.public = 1
            note.save()
            frappe.db.commit()
            return Response(challenge, status=200)
            # return challenge, 200
        else:
            note.public = 0
            note.save()
            frappe.db.commit()
            return response(status_code=403)
    if note.content:
        note.content = note.content + "<br><br>" + "in if else"
    else:
        note.content = "in if else"
    note.save()
    frappe.db.commit()
    return response(status_code=403)

@frappe.whitelist(allow_guest=True)
def response(status_code, message=None):
    frappe.clear_messages()
    """
    Params: message, status code
    """
    frappe.local.response["message"] = message
    frappe.local.response["status_code"] = status_code
    return
