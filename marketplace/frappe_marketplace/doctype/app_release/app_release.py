# Copyright (c) 2026, BWH and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AppRelease(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		app: DF.Link | None
		author: DF.Data | None
		branch: DF.Data | None
		ci_log_url: DF.Data | None
		ci_status: DF.Literal["Pending", "Running", "Passed", "Failed"]
		hash: DF.Data | None
		invalid_release: DF.Check
		invalidation_reason: DF.Code | None
		message: DF.SmallText | None
		publisher: DF.Link | None
		source: DF.Link | None
		status: DF.Literal["Draft", "Approved", "Awaiting Approval", "Rejected"]
		validation_logs: DF.LongText | None
	# end: auto-generated types

	pass
