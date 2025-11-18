import frappe
import requests

def send_larksuite_notification(user, passed, scores=None):
    webhook_url = frappe.conf.get("larksuite_webhook_url")
    if not webhook_url:
        frappe.logger().warning("Larksuite webhook URL not set in site_config.json")
        return

    user_details = frappe.get_value("User", user, ["email", "crew_rank"], as_dict=True)
    if not user_details:
        frappe.logger().error(f"Could not find user {user}")
        return

    job_role = None
    if user_details.crew_rank:
        job_role = frappe.db.get_value("Crew Rank", user_details.crew_rank, "rank_name")

    payload = {
        "email": user_details.email,
        "job_role": job_role,
        "passed": passed,
    }

    if scores:
        payload["scores"] = scores

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        frappe.logger().info(f"Sent notification to Larksuite for user {user_details.email}")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Failed to send notification to Larksuite for user {user_details.email}")
