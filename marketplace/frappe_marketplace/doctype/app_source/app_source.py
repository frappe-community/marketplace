# Copyright (c) 2025, BWH and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AppSource(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from marketplace.frappe_marketplace.doctype.app_source_version.app_source_version import (
			AppSourceVersion,
		)
		from marketplace.frappe_marketplace.doctype.required_apps.required_apps import RequiredApps

		app: DF.Link | None
		app_title: DF.Data | None
		branch: DF.Data | None
		current_release: DF.Link | None
		enabled: DF.Check
		frappe: DF.Check
		github_installation_id: DF.Data | None
		github_repo_full_name: DF.Data | None
		last_github_poll_failed: DF.Check
		last_github_response: DF.Code | None
		last_synced: DF.Datetime | None
		public: DF.Check
		publisher: DF.Link | None
		repository: DF.Data | None
		repository_owner: DF.Data | None
		repository_url: DF.Data | None
		required_apps: DF.Table[RequiredApps]
		uninstalled: DF.Check
		versions: DF.Table[AppSourceVersion]
	# end: auto-generated types

	pass
