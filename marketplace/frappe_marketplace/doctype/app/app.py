# Copyright (c) 2025, BWH and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class App(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		app_name: DF.Data
		branch: DF.Data | None
		enable_auto_deploy: DF.Check
		enabled: DF.Check
		frappe: DF.Check
		installation: DF.Data | None
		public: DF.Check
		publisher: DF.Link | None
		repo: DF.Data | None
		repo_owner: DF.Data | None
		scrubbed: DF.Data | None
		skip_review: DF.Check
		title: DF.Data
		url: DF.Data | None
	# end: auto-generated types

	pass
