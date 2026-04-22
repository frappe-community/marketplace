app_name = "marketplace"
app_title = "Frappe Marketplace"
app_publisher = "BWH"
app_description = "Publishing platform for Frappe Apps"
app_email = "developers@buildwithhussain.com"
app_license = "agpl-3.0"

# Apps
# ------------------
website_route_rules = [
	{
		"from_route": "/dashboard/<path:app_path>",
		"to_route": "dashboard",
	},
]

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "marketplace",
# 		"logo": "/assets/marketplace/logo.png",
# 		"title": "Frappe Marketplace",
# 		"route": "/marketplace",
# 		"has_permission": "marketplace.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/marketplace/css/marketplace.css"
# app_include_js = "/assets/marketplace/js/marketplace.js"

# include js, css files in header of web template
# web_include_css = "/assets/marketplace/css/marketplace.css"
# web_include_js = "/assets/marketplace/js/marketplace.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "marketplace/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "marketplace/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }
role_home_page = {"Marketplace Publisher": "/dashboard"}
# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "marketplace.utils.jinja_methods",
# 	"filters": "marketplace.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "marketplace.install.before_install"
# after_install = "marketplace.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "marketplace.uninstall.before_uninstall"
# after_uninstall = "marketplace.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "marketplace.utils.before_app_install"
# after_app_install = "marketplace.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "marketplace.utils.before_app_uninstall"
# after_app_uninstall = "marketplace.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "marketplace.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"User": {"on_update": "marketplace.api.github.add_publisher_role_on_github_login"}
	# 	"*": {
	# 		"on_update": "method",
	# 		"on_cancel": "method",
	# 		"on_trash": "method"
	# 	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"marketplace.tasks.all"
# 	],
# 	"daily": [
# 		"marketplace.tasks.daily"
# 	],
# 	"hourly": [
# 		"marketplace.tasks.hourly"
# 	],
# 	"weekly": [
# 		"marketplace.tasks.weekly"
# 	],
# 	"monthly": [
# 		"marketplace.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "marketplace.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "marketplace.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "marketplace.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "marketplace.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["marketplace.utils.before_request"]
# after_request = ["marketplace.utils.after_request"]

# Job Events
# ----------
# before_job = ["marketplace.utils.before_job"]
# after_job = ["marketplace.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"marketplace.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
