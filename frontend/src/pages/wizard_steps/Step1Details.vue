<template>
	<div class="grid grid-cols-1 gap-8 lg:grid-cols-12 items-start">
		<div class="lg:col-span-8 flex flex-col gap-10">
			<section class="flex flex-col gap-4">
				<div class="px-1">
					<h2 class="text-sm font-bold uppercase tracking-widest text-gray-500">
						Basic Info
					</h2>
				</div>

				<div class="flex flex-col gap-5">
					<div class="flex flex-col gap-1.5">
						<label class="text-xs text-gray-600 ml-1">App Title</label>
						<TextInput
							v-model="form.app_title"
							placeholder="e.g. Library Management"
						/>
					</div>

					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<div class="flex flex-col gap-1.5">
							<label
								class="text-[10px] font-bold uppercase tracking-wider text-gray-400 ml-1"
								>Internal Name</label
							>
							<div
								class="px-3 py-2 rounded-lg bg-gray-50 border border-gray-100 text-sm text-gray-600 font-mono"
							>
								{{ form.app_name || "---" }}
							</div>
						</div>

						<div class="flex flex-col gap-1.5">
							<label
								class="text-[10px] font-bold uppercase tracking-wider text-gray-400 ml-1"
								>Repository URL</label
							>
							<div
								class="px-3 py-2 rounded-lg bg-gray-50 border border-gray-100 text-sm text-gray-600 break-all font-mono leading-relaxed"
							>
								{{ form.repo_url || "---" }}
							</div>
						</div>
					</div>
				</div>
			</section>

			<section class="flex flex-col gap-4">
				<div class="flex items-center justify-between px-1">
					<h2 class="text-sm font-bold uppercase tracking-widest text-gray-500">
						Compatibility
					</h2>
					<Button variant="outline" size="sm" @click="addRow">
						<template #prefix>
							<FeatherIcon name="plus" class="w-4 h-4" />
						</template>
						Add another version
					</Button>
				</div>

				<div class="flex flex-col gap-4">
					<div
						v-for="(row, index) in form.versions"
						:key="index"
						class="p-5 border rounded-xl bg-white dark:bg-gray-900 shadow-sm transition-shadow hover:shadow-md"
					>
						<div class="flex flex-col gap-6 md:flex-row md:items-end">
							<div class="flex-1 flex flex-col gap-1.5">
								<label class="text-[10px] font-bold uppercase text-gray-400 ml-1"
									>Frappe Version</label
								>
								<Select
									:options="frappeVersionOptions"
									v-model="row.version"
									placeholder="Select Version"
								/>
							</div>

							<div class="hidden md:flex items-center justify-center pb-2.5">
								<FeatherIcon name="arrow-right" class="h-4 w-4 text-gray-300" />
							</div>

							<div class="flex-1 flex flex-col gap-1.5">
								<label class="text-[10px] font-bold uppercase text-gray-400 ml-1"
									>Branch</label
								>
								<Autocomplete
									:options="branchOptions"
									v-model="row.branch"
									placeholder="Search branch"
								/>
							</div>

							<div class="flex justify-end md:pb-0.5">
								<Button
									variant="ghost"
									theme="red"
									icon="trash-2"
									@click="askRemove(index)"
								/>
							</div>
						</div>
					</div>

					<div
						v-if="!form.versions || !form.versions.length"
						class="flex flex-col items-center justify-center py-12 border-2 border-dashed rounded-xl bg-gray-50/50"
					>
						<p class="text-sm text-gray-500 italic">
							No compatibility versions added.
						</p>
						<Button variant="link" label="Add your first version" @click="addRow" />
					</div>
				</div>
			</section>
		</div>

		<div class="lg:col-span-4 flex flex-col gap-6 lg:sticky lg:top-24">
			<div class="p-6 border rounded-xl bg-white dark:bg-gray-900 shadow-sm">
				<h3 class="mb-5 text-xs font-bold uppercase text-gray-500 tracking-wider">
					App Logo
				</h3>
				<div class="flex flex-col items-center gap-5">
					<div
						class="flex h-24 w-24 items-center justify-center rounded-2xl border-2 border-dashed bg-gray-50 dark:bg-gray-800 overflow-hidden"
					>
						<img
							v-if="form.logo"
							:src="form.logo"
							class="h-full w-full object-cover"
						/>
						<FeatherIcon v-else name="image" class="h-8 w-8 text-gray-300" />
					</div>
					<FileUploader @success="(file) => (form.logo = file.file_url)" class="w-full">
						<template #default="{ openFileSelector, uploading }">
							<Button
								variant="outline"
								class="w-full"
								:label="uploading ? 'Uploading...' : 'Upload Logo'"
								@click="openFileSelector"
							/>
						</template>
					</FileUploader>
				</div>
			</div>

			<div
				class="p-6 border border-blue-100 bg-blue-50/30 dark:bg-blue-900/10 dark:border-blue-900/30 rounded-xl"
			>
				<div class="mb-4 flex items-center gap-2 text-blue-700 dark:text-blue-400">
					<FeatherIcon name="cpu" class="h-4 w-4" />
					<h3 class="text-xs font-bold uppercase tracking-wider">Requirements</h3>
				</div>

				<div v-if="loadingMeta" class="py-2 flex justify-center">
					<LoadingIndicator class="w-5 h-5 text-blue-500" />
				</div>

				<div v-else class="flex flex-col gap-4">
					<div
						v-if="frappeRequirement"
						class="p-3 bg-white dark:bg-gray-900 rounded-lg border border-blue-100 dark:border-blue-800 shadow-sm"
					>
						<p class="text-[10px] font-bold uppercase text-blue-500 mb-1">Framework</p>
						<p
							class="text-sm font-semibold text-gray-900 dark:text-white leading-none"
						>
							Frappe {{ frappeRequirement }}
						</p>
					</div>

					<div class="flex flex-col gap-2">
						<p class="text-[10px] font-bold uppercase text-blue-500 ml-1">
							Dependencies
						</p>
						<div class="flex flex-wrap gap-2">
							<Badge
								v-for="app in dependencies"
								:key="app"
								theme="blue"
								variant="subtle"
							>
								{{ app }}
							</Badge>
							<p
								v-if="!dependencies || !dependencies.length"
								class="text-xs italic text-gray-500"
							>
								None detected
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>

		<Dialog
			v-model="showDeleteDialog"
			:options="{
				title: 'Remove Mapping',
				message: 'Are you sure you want to remove this version mapping?',
				size: 'sm',
			}"
		>
			<template #actions>
				<div class="flex gap-2 w-full">
					<Button class="flex-1" label="Cancel" @click="showDeleteDialog = false" />
					<Button
						class="flex-1"
						variant="solid"
						theme="red"
						label="Remove"
						@click="removeRowConfirmed"
					/>
				</div>
			</template>
		</Dialog>
	</div>
</template>

<script setup>
import { computed, ref } from "vue";
import {
	TextInput,
	Select,
	Autocomplete,
	Badge,
	Button,
	FeatherIcon,
	FileUploader,
	LoadingIndicator,
	Dialog,
	createResource,
} from "frappe-ui";

const props = defineProps({
	form: {
		type: Object,
		default: () => ({ versions: [], app_title: "", logo: "" }),
	},
	branches: {
		type: Array,
		default: () => [],
	},
	dependencies: {
		type: Array,
		default: () => [],
	},
	loadingMeta: {
		type: Boolean,
		default: false,
	},
	frappeRequirement: {
		type: String,
		default: "",
	},
});

const showDeleteDialog = ref(false);
const rowToDelete = ref(null);

const branchOptions = computed(() => {
	return props.branches ? props.branches.map((b) => ({ label: b, value: b })) : [];
});

const versionsResource = createResource({
	url: "frappe.client.get_list",
	params: {
		doctype: "Frappe Version",
		fields: ["name"],
		filters: { public: 1 },
		order_by: "number desc",
	},
	auto: true,
});

const frappeVersionOptions = computed(() => {
	if (!versionsResource.data) return [];
	return versionsResource.data.map((v) => ({
		label: v.name,
		value: v.name,
	}));
});

function addRow() {
	if (!props.form.versions) {
		props.form.versions = [];
	}
	props.form.versions.push({ version: "", branch: "" });
}

function askRemove(index) {
	rowToDelete.value = index;
	showDeleteDialog.value = true;
}

function removeRowConfirmed() {
	if (rowToDelete.value !== null) {
		props.form.versions.splice(rowToDelete.value, 1);
	}
	showDeleteDialog.value = false;
	rowToDelete.value = null;
}
</script>
