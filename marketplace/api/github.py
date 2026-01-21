import frappe
from frappe.utils.oauth import get_oauth2_authorize_url


@frappe.whitelist(allow_guest=True)
def get_github_auth_url():
    provider = "github"
    redirect_to = "/dashboard"

    auth_url = get_oauth2_authorize_url(provider, redirect_to)

    return auth_url
