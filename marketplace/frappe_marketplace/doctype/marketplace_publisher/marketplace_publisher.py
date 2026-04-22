# Copyright (c) 2025, BWH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MarketplacePublisher(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		company_name: DF.Data | None
		contact_email: DF.Data | None
		github_access_token: DF.Password | None
		github_username: DF.Data | None
		is_setup_complete: DF.Check
		logo: DF.AttachImage | None
		publisher_name: DF.Data | None
		publisher_type: DF.Literal["Individual", "Organization"]
		user: DF.Link | None
		website: DF.Data | None
	# end: auto-generated types
