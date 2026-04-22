<template>
	<div class="p-6 max-w-6xl mx-auto">
		<div v-if="loading" class="flex justify-center py-20">
			<LoadingIndicator class="w-8 h-8" />
		</div>

		<div v-else-if="!app" class="text-center text-red-500 py-20">App not found</div>

		<div v-else class="space-y-6">
			<Card>
				<div class="flex items-center justify-between">
					<div>
						<h1 class="text-3xl font-semibold">{{ app.app }}</h1>
						<p class="text-gray-500 mt-1">
							{{ app.description || "No description provided" }}
						</p>
						<p class="text-sm text-gray-500 mt-2">
							Published by <span class="font-medium">{{ app.publisher_name }}</span>
						</p>
					</div>

					<Badge :theme="statusTheme(app.status)">
						{{ app.status }}
					</Badge>
				</div>
			</Card>

			<Tabs
				class="border rounded-2xl overflow-hidden bg-white dark:bg-gray-900"
				v-model="activeTabIndex"
				:tabs="tabs"
			>
				<template #tab-panel="{ tab }">
					<div v-if="tab.key === 'releases'" class="p-6 space-y-6">
						<div v-if="releasesResource.loading" class="flex justify-center py-16">
							<LoadingIndicator class="w-6 h-6" />
						</div>

						<div
							v-else-if="releasesResource.data?.length === 0"
							class="text-center py-16 text-gray-500"
						>
							No releases yet. Create a new version from the wizard.
						</div>
						<div v-else class="space-y-4">
							<Card
								v-for="release in releasesResource.data"
								:key="release.name"
								class="hover:shadow-md transition"
							>
								<div class="flex items-center justify-between">
									<div>
										<p class="font-semibold">{{ release.name }}</p>
										<p class="text-sm text-gray-500">
											Branch:
											<span class="font-medium">{{ release.branch }}</span>
										</p>
										<p class="text-xs text-gray-400">
											Created
											{{ new Date(release.creation).toLocaleString() }}
										</p>
									</div>

									<div class="flex gap-3">
										<Badge :theme="ciTheme(release.ci_status)">
											CI {{ release.ci_status }}
										</Badge>
										<Badge :theme="releaseTheme(release.status)">
											{{ release.status }}
										</Badge>
									</div>
								</div>

								<div
									v-if="release.hash"
									class="mt-4 text-xs bg-gray-50 dark:bg-gray-800 px-3 py-2 rounded"
								>
									Commit: <span class="font-mono">{{ release.hash }}</span>
								</div>
							</Card>
						</div>
					</div>

					<div v-else-if="tab.key === 'overview'" class="p-6 space-y-6">
						<Card title="Long Description">
							<div
								class="prose max-w-none dark:prose-invert"
								v-html="app.long_description || app.description"
							/>
						</Card>

						<Card title="Details">
							<div class="grid grid-cols-2 gap-6">
								<div>
									<p class="text-sm text-gray-500">Publisher</p>
									<p class="font-medium">{{ app.publisher_name }}</p>
								</div>

								<div>
									<p class="text-sm text-gray-500">Repository</p>
									<a
										:href="app.url"
										target="_blank"
										class="text-blue-600 hover:underline"
									>
										View Repository →
									</a>
								</div>

								<div>
									<p class="text-sm text-gray-500">Status</p>
									<Badge :theme="statusTheme(app.status)">
										{{ app.status }}
									</Badge>
								</div>

								<div>
									<p class="text-sm text-gray-500">App Name</p>
									<p class="font-medium">{{ app.app }}</p>
								</div>
							</div>
						</Card>
					</div>

					<div v-else-if="tab.key === 'settings'" class="p-6 space-y-6">
						<Card title="Latest Release">
							<div v-if="latestRelease" class="flex justify-between items-center">
								<div>
									<p class="font-medium">{{ latestRelease.name }}</p>
									<p class="text-sm text-gray-500">
										Branch: {{ latestRelease.branch }}
									</p>
								</div>

								<Badge :theme="ciTheme(latestRelease.ci_status)">
									CI {{ latestRelease.ci_status }}
								</Badge>
							</div>

							<div v-else class="text-gray-500">No release available.</div>
						</Card>
						<Card title="Submission">
							<div class="space-y-4">
								<div class="text-sm text-gray-600">
									Submit your app for Marketplace review. CI must pass first.
								</div>

								<Button
									appearance="primary"
									:disabled="!canSubmitForReview || submitForReview.loading"
									@click="handleSubmitForReview"
								>
									Submit for Review
								</Button>

								<p v-if="!canSubmitForReview" class="text-xs text-gray-500">
									CI must pass before submission.
								</p>
							</div>
						</Card>

						<Card title="Danger Zone">
							<div class="space-y-4">
								<p class="text-sm text-gray-600">
									Deleting your app permanently removes releases and sources.
								</p>

								<Button
									variant="solid"
									theme="red"
									@click="showDeleteDialog = true"
								>
									Delete App Permanently
								</Button>
							</div>
						</Card>

						<Dialog
							v-model="showDeleteDialog"
							:options="{
								title: 'Delete this app permanently?',
								message: 'This action cannot be undone.',
								size: 'sm',
							}"
						>
							<template #actions>
								<div class="flex flex-row justify-end gap-3 w-full">
									<Button variant="ghost" @click="showDeleteDialog = false">
										Cancel
									</Button>
									<Button
										variant="solid"
										theme="red"
										:loading="deleteAppResource.loading"
										@click="confirmDeleteApp"
									>
										Delete App
									</Button>
								</div>
							</template>
						</Dialog>
					</div>
				</template>
			</Tabs>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { createResource, Card, Badge, Tabs, LoadingIndicator, Dialog, Button } from "frappe-ui";
import { LucideRocket, LucideInfo, LucideSettings } from "lucide-vue-next";

const route = useRoute();
const router = useRouter();

const app = ref(null);
const loading = ref(true);
const showDeleteDialog = ref(false);
const activeTabIndex = ref(0);

const tabs = [
	{ label: "Overview", key: "overview", icon: LucideInfo },
	{ label: "Releases", key: "releases", icon: LucideRocket },
	{ label: "Settings", key: "settings", icon: LucideSettings },
];

const appResource = createResource({
	url: "frappe.client.get_value",
	params: {
		doctype: "Marketplace App",
		filters: { app: route.params.app_name },
		fieldname: [
			"name",
			"app",
			"description",
			"long_description",
			"publisher.publisher_name as publisher_name",
			"status",
			"url",
		],
	},
});

const releasesResource = createResource({
	url: "frappe.client.get_list",
	params: {
		doctype: "App Release",
		filters: { app: route.params.app_name },
		fields: ["name", "branch", "status", "ci_status", "hash", "creation"],
		order_by: "creation desc",
	},
	auto: true,
});

const submitForReview = createResource({
	url: "marketplace.api.setup_wizard.finalize_submission",
});

const deleteAppResource = createResource({
	url: "marketplace.api.setup_wizard.delete_marketplace_app",
});

const latestRelease = computed(() => releasesResource.data?.[0] || null);
const canSubmitForReview = computed(
	() => latestRelease.value?.ci_status === "Passed" && app.value?.status === "Draft"
);

async function handleSubmitForReview() {
	if (!latestRelease.value) return;
	await submitForReview.fetch({ app_release_id: latestRelease.value.name });
	await appResource.fetch();
	await releasesResource.fetch();
}

async function confirmDeleteApp() {
	await deleteAppResource.fetch({ app_name: app.value.name });
	showDeleteDialog.value = false;
	router.push("/dashboard/my-apps");
}

const statusTheme = (s) =>
	({ Draft: "gray", "In Review": "orange", Published: "green", Rejected: "red" }[s] || "gray");
const ciTheme = (s) => ({ Running: "orange", Passed: "green", Failed: "red" }[s] || "gray");
const releaseTheme = (s) =>
	({ Draft: "gray", "In Review": "orange", Published: "green", Rejected: "red" }[s] || "gray");

onMounted(async () => {
	app.value = await appResource.fetch();
	loading.value = false;
});
</script>
