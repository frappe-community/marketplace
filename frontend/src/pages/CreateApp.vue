<template>
	<div class="max-w-6xl mx-auto space-y-8">
		<div class="space-y-1">
			<h1 class="text-2xl font-semibold text-gray-900">Select Repository</h1>
			<p class="text-gray-500">
				Choose the GitHub repository you want to publish on Marketplace.
			</p>
		</div>

		<div class="bg-white rounded-2xl shadow-sm border">
			<ListView
				v-if="!reposResource.loading"
				:columns="columns"
				:rows="rows"
				:options="options"
				row-key="id"
			/>

			<div v-else class="flex justify-center py-16 text-gray-500">
				Loading repositories...
			</div>

			<div
				v-if="!reposResource.loading && rows.length === 0"
				class="flex justify-center py-16 text-gray-500"
			>
				No repositories found.
			</div>
		</div>
	</div>
</template>

<script setup>
import { h, computed } from "vue";
import { useRouter } from "vue-router";
import { Avatar, Badge, ListView, createResource } from "frappe-ui";

const router = useRouter();

const reposResource = createResource({
	url: "marketplace.api.github.get_publisher_repos",
	auto: true,
});

const columns = [
	{
		label: "Repository",
		key: "name",
		width: 3,
		getLabel: ({ row }) => row.name,
	},
];

const rows = computed(() => reposResource.data || []);

const options = {
	selectable: false,
	resizeColumn: true,
	showTooltip: true,

	onRowClick: (row) => {
		router.push({
			name: "ManageApp",
			params: { appName: "new" }, // required param
			query: {
				repo_url: row.html_url,
				repo_name: row.name,
				repo_description: row.description || "",
			},
		});
	},
};
</script>
