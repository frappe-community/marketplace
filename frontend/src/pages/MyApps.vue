<template>
	<div class="bg-white rounded-lg border border-gray-200 p-4">
		<div class="flex items-center justify-between mb-4">
			<h2 class="text-lg font-semibold text-gray-800">My Apps</h2>

			<Button variant="solid" @click="goToSetup"> Create New App </Button>
		</div>

		<ListView
			:columns="columns"
			:rows="appsResource.data || []"
			row-key="name"
			:options="{
				selectable: false,
				resizeColumn: true,
				showTooltip: true,
			}"
		>
			<ListHeader>
				<ListHeaderItem v-for="column in columns" :key="column.key" :item="column">
					<template #prefix="{ item }">
						<component :is="item.icon" class="size-4" />
					</template>
				</ListHeaderItem>
			</ListHeader>

			<ListRows>
				<ListRow
					v-for="row in appsResource.data"
					:key="row.name"
					:row="row"
					class="cursor-pointer hover:bg-gray-50 transition"
					@click="goToApp(row)"
					v-slot="{ column, item }"
				>
					<ListRowItem>
						<!-- STATUS COLUMN -->
						<template v-if="column.key === 'status'">
							<div class="flex items-center gap-2">
								<div class="h-3 w-3 rounded-full" :class="item.bg_color" />
								<span class="text-sm text-gray-700">
									{{ item.label }}
								</span>
							</div>
						</template>

						<template v-else>
							{{ item }}
						</template>
					</ListRowItem>
				</ListRow>
			</ListRows>

			<template #empty-state>
				<div class="text-center py-10 text-gray-500">No apps found.</div>
			</template>
		</ListView>
	</div>
</template>

<script setup>
import { reactive } from "vue";
import { createListResource } from "frappe-ui";
import { useRouter } from "vue-router";

const router = useRouter();

import {
	ListHeader,
	ListHeaderItem,
	ListRow,
	ListRowItem,
	ListRows,
	ListView,
	Button,
} from "frappe-ui";

import LucidePackage from "~icons/lucide/package";
import LucideCheckCircle from "~icons/lucide/check-circle";

const columns = reactive([
	{ label: "App Name", key: "app", icon: LucidePackage },
	{ label: "Status", key: "status", icon: LucideCheckCircle },
]);

function getStatusBg(status) {
	const map = {
		Draft: "bg-surface-gray-4",
		Published: "bg-surface-green-3",
		"In Review": "bg-surface-blue-3",
		"Attention Required": "bg-surface-orange-3",
		Rejected: "bg-surface-red-4",
		Disabled: "bg-surface-gray-5",
	};

	return map[status] || "bg-surface-gray-4";
}

const appsResource = createListResource({
	doctype: "Marketplace App",
	fields: ["name", "app", "status"],
	auto: true,
	transform(data) {
		return data.map((app) => ({
			...app,
			status: {
				label: app.status,
				bg_color: getStatusBg(app.status),
			},
		}));
	},
});

function goToApp(row) {
	router.push(`/dashboard/my-apps/${row.name}`);
}

function goToSetup() {
	router.push("/dashboard/create-app");
}
</script>
