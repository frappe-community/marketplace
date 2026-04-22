<template>
	<div class="p-6 max-w-4xl mx-auto space-y-6">
		<Card title="Publisher Profile">
			<template #actions>
				<Button variant="solid" :loading="updateResource.loading" @click="saveProfile">
					Save Changes
				</Button>
			</template>

			<div v-if="publisherResource.loading" class="flex items-center justify-center p-12">
				<LoadingIndicator class="w-8 h-8" />
			</div>

			<div v-else-if="publisherResource.data" class="space-y-8">
				<div class="flex items-center gap-6">
					<FileUploader @success="(file) => (editableForm.logo = file.file_url)">
						<template #default="{ openFileSelector }">
							<button
								@click="openFileSelector"
								class="w-24 h-24 rounded-2xl bg-gray-50 border border-gray-200 flex items-center justify-center overflow-hidden hover:bg-gray-100 transition-colors"
							>
								<img
									v-if="editableForm.logo"
									:src="editableForm.logo"
									class="w-full h-full object-cover"
								/>
								<FeatherIcon v-else name="image" class="w-10 h-10 text-gray-400" />
							</button>
						</template>
					</FileUploader>

					<div class="flex-1 space-y-3">
						<TextInput label="Publisher Name" v-model="editableForm.publisher_name" />

						<div class="flex gap-4">
							<Select
								label="Type"
								class="flex-1"
								:options="[
									{ label: 'Individual', value: 'Individual' },
									{ label: 'Organization', value: 'Organization' },
								]"
								v-model="editableForm.publisher_type"
							/>
							<TextInput
								label="Contact Email"
								class="flex-1"
								v-model="editableForm.contact_email"
							/>
						</div>
					</div>
				</div>

				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<TextInput
						label="Website"
						v-model="editableForm.website"
						placeholder="https://..."
					/>
					<TextInput label="Company Name" v-model="editableForm.company_name" />
				</div>
			</div>
		</Card>

		<Card title="Published Apps">
			<div v-if="appsResource.loading" class="p-4 text-gray-500">Loading apps...</div>

			<div v-else-if="appsResource.data?.length" class="divide-y divide-gray-100">
				<div
					v-for="app in appsResource.data"
					:key="app.name"
					class="py-4 flex items-center justify-between"
				>
					<div class="flex items-center gap-4">
						<div
							class="w-10 h-10 rounded bg-gray-100 flex items-center justify-center"
						>
							<img
								v-if="app.app_logo"
								:src="app.app_logo"
								class="w-full h-full object-contain"
							/>
							<FeatherIcon v-else name="package" class="w-5 h-5 text-gray-400" />
						</div>

						<div>
							<p class="font-medium text-gray-900">{{ app.title }}</p>
							<p class="text-xs text-gray-500">{{ app.app_name }}</p>
						</div>
					</div>

					<Badge theme="gray">{{ app.status }}</Badge>
				</div>
			</div>

			<div v-else class="p-8 text-center text-gray-500 italic">No apps published yet.</div>
		</Card>
	</div>
</template>

<script setup>
import { reactive } from "vue";
import {
	createResource,
	Card,
	Badge,
	FeatherIcon,
	LoadingIndicator,
	TextInput,
	Button,
	Select,
	FileUploader,
} from "frappe-ui";
import { session } from "@/data/session";

const editableForm = reactive({
	publisher_name: "",
	publisher_type: "",
	contact_email: "",
	website: "",
	company_name: "",
	logo: "",
});

const publisherResource = createResource({
	url: "frappe.client.get",
	params: {
		doctype: "Marketplace Publisher",
		name: session.user,
	},
	auto: true,
	onSuccess(data) {
		Object.assign(editableForm, data);
	},
});

const updateResource = createResource({
	url: "frappe.client.set_value",
	onSuccess() {
		publisherResource.reload();
		frappe.show_alert({ message: "Profile updated", indicator: "green" });
	},
});

function saveProfile() {
	updateResource.submit({
		doctype: "Marketplace Publisher",
		name: session.user,
		fieldname: editableForm,
	});
}

const appsResource = createResource({
	url: "frappe.client.get_list",
	params: {
		doctype: "Marketplace App",
		filters: { publisher: session.user },
		fields: ["name", "title", "description", "status", "image"],
		order_by: "creation desc",
	},
	auto: true,
});
</script>
