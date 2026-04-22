import re
import base64
import frappe
import tomllib
from packaging import specifiers
import requests
from frappe import _
from packaging.version import Version
from frappe.utils.oauth import get_oauth2_authorize_url

# Helpers

def get_connected_app():
    connected_app_name = frappe.db.get_value(
        "Connected App",
        {"provider_name": "Github"},
        "name"
    )
    if not connected_app_name:
        frappe.throw(_("Marketplace Connected App not found."))

    return frappe.get_doc("Connected App", connected_app_name)


def get_github_token():
    connected_app = get_connected_app()
    token_cache = connected_app.get_token_cache(frappe.session.user)

    if not token_cache:
        frappe.throw(_("No token found. Please authorize GitHub."))

    return token_cache.get_password("access_token")


def get_github_headers():
    token = get_github_token()
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }


# OAuth / Login

@frappe.whitelist(allow_guest=True) # nosemgrep
def get_github_login_url():
    return get_oauth2_authorize_url("github", "/dashboard")


@frappe.whitelist(allow_guest=True) # nosemgrep
def get_github_auth_url():
    frontend_url = frappe.conf.get("frontend_url") or frappe.utils.get_url()
    success_uri = f"{frontend_url}/publishersetup"
    connected_app = get_connected_app()
    return connected_app.initiate_web_application_flow(success_uri=success_uri)


@frappe.whitelist()
def check_if_connected():
    connected_app = get_connected_app()
    return frappe.db.exists(
        "Token Cache",
        {
            "connected_app": connected_app.name,
            "user": frappe.session.user
        }
    )

# User Role Logic

def add_publisher_role_on_github_login(doc, method):
    role_name = "Marketplace Publisher"

    if not frappe.db.exists("Role", role_name):
        return

    if frappe.db.exists(
        "User Social Login",
        {
            "parent": doc.name,
            "provider": "github"
        }
    ):
        doc.add_roles(role_name)


# GitHub API

@frappe.whitelist()
def get_github_profile_data():
    headers = get_github_headers()
    res = requests.get("https://api.github.com/user", headers=headers)

    if res.status_code == 401:
        frappe.log_error(
            "GitHub 401: Invalid or expired token",
            "GitHub Integration"
        )
        return {"message": "Bad credentials", "status": "401"}

    return res.json()


@frappe.whitelist()
def get_publisher_repos():
    headers = get_github_headers()
    res = requests.get(
        "https://api.github.com/user/repos?type=owner&sort=updated",
        headers=headers
    )
    if res.status_code != 200:
        frappe.log_error(
            f"GitHub repos fetch failed: {res.status_code} {res.text}",
            "GitHub Integration"
        )
        return []
    return res.json()

@frappe.whitelist()
def fetch_repo_info(repo_url: str):
    parts = repo_url.rstrip("/").split("/")
    owner, repo_name = parts[-2], parts[-1]
    headers = get_github_headers()

    default_branch, branches, raw_github_data = get_repo_and_branches(owner, repo_name, headers)

    toml_str = fetch_toml_content(owner, repo_name, headers)

    repo_description = raw_github_data.get("description", "")
    toml_metadata = {}
    if toml_str:
        toml_metadata = extract_toml_metadata(toml_str, repo_name) or {}

    metadata = {
        "app_name": toml_metadata.get("app_name") or repo_name,
        "app_title": (
            toml_metadata.get("app_title")
            or repo_name
        ),
        "app_description": (
            toml_metadata.get("app_description")
            or repo_description
            or ""
        ),
        "dependencies": toml_metadata.get("dependencies") or [],
        "frappe_version_requirement": (
            toml_metadata.get("frappe_version_requirement")
            or ">=15.0.0,<16.0.0"
        ),
    }

    if not metadata.get("frappe_version_requirement"):
        metadata["frappe_version_requirement"] = ">=15.0.0,<16.0.0"

    if not metadata.get("dependencies"):
        metadata["dependencies"] = []

    return {
        "branches": branches,
        "default_branch": default_branch,
        "metadata": metadata,
        "raw_github_data": raw_github_data
    }

def get_repo_and_branches(owner, repo_name, headers):
    repo_res = requests.get(
        f"https://api.github.com/repos/{owner}/{repo_name}",
        headers=headers
    )
    branches_res = requests.get(
        f"https://api.github.com/repos/{owner}/{repo_name}/branches",
        headers=headers
    )

    raw_repo_data = repo_res.json() if repo_res.status_code == 200 else {}
    default_branch = raw_repo_data.get("default_branch", "main")

    branches = []
    if branches_res.status_code == 200:
        branches = [b["name"] for b in branches_res.json()]

    return default_branch, branches, raw_repo_data

def fetch_toml_content(owner, repo_name, headers):
    res = requests.get(
        f"https://api.github.com/repos/{owner}/{repo_name}/contents/pyproject.toml",
        headers=headers,
        timeout=10
    )
    if res.status_code != 200:
        return None
    return base64.b64decode(res.json()["content"]).decode("utf-8")

def extract_toml_metadata(toml_str, fallback_name):
    try:
        data = tomllib.loads(toml_str)
    except Exception:
        frappe.log_error(title="TOML Parse Failure", message=frappe.get_traceback())
        return {}

    project = data.get("project", {})
    dependencies = project.get("dependencies", [])

    frappe_req = None
    for dep in dependencies:
        if dep.lower().startswith("frappe"):
            match = re.match(r"frappe\s*([<>=!~].+)", dep, re.IGNORECASE)
            if match:
                frappe_req = match.group(1)
            break

    if not frappe_req:
        bench_tool = data.get("tool", {}).get("bench", {})
        frappe_req = (
            bench_tool.get("frappe-dependencies", {}).get("frappe") or
            bench_tool.get("frappe_dependencies", {}).get("frappe")
        )

    result = {
        "app_name": project.get("name", fallback_name),
        "app_title": project.get("name", fallback_name),
        "app_description": project.get("description", ""),
        "dependencies": dependencies,
        "frappe_version_requirement": frappe_req,
    }

    return result

@frappe.whitelist()
def check_version_compatibility(required_range: str, user_version: str):
    if not required_range:
        return True

    try:
        spec = specifiers.SpecifierSet(required_range)
        version = Version(user_version)
        return version in spec
    except Exception:
        frappe.log_error(
            title="Version Check Exception",
            message=frappe.get_traceback()
        )
        return False
