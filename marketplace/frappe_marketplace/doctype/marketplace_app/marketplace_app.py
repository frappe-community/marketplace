# Copyright (c) 2025, BWH and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class MarketplaceApp(WebsiteGenerator):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from marketplace.frappe_marketplace.doctype.marketplace_app_categories.marketplace_app_categories import (
			MarketplaceAppCategories,
		)
		from marketplace.frappe_marketplace.doctype.marketplace_app_screenshot.marketplace_app_screenshot import (
			MarketplaceAppScreenshot,
		)
		from marketplace.frappe_marketplace.doctype.marketplace_app_version.marketplace_app_version import (
			MarketplaceAppVersion,
		)

		app: DF.Link
		categories: DF.Table[MarketplaceAppCategories]
		description: DF.SmallText | None
		documentation: DF.Data | None
		image: DF.AttachImage | None
		long_description: DF.TextEditor | None
		privacy_policy: DF.Data | None
		published: DF.Check
		published_on: DF.Date | None
		publisher: DF.Link | None
		route: DF.Data | None
		screenshots: DF.Table[MarketplaceAppScreenshot]
		sources: DF.Table[MarketplaceAppVersion]
		status: DF.Literal["Draft", "Published", "In Review", "Attention Required", "Rejected", "Disabled"]
		support: DF.Data | None
		terms_of_service: DF.Data | None
		title: DF.Data
		url: DF.Data | None
		website: DF.Data | None
	# end: auto-generated types

	pass
