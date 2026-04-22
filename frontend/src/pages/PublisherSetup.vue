<template>
	<div class="min-h-screen bg-black flex items-center justify-center p-4">
		<div class="w-full max-w-2xl bg-[#111111] border border-gray-800 rounded-2xl p-8">
			<div class="mb-8">
				<h2 class="text-2xl font-semibold text-white">Setup publisher profile</h2>
				<p class="text-gray-400 text-sm mt-1">Link your GitHub account to get started.</p>
			</div>

			<div
				v-if="errorMessage"
				class="mb-6 p-3 bg-red-900/30 border border-red-800 rounded-lg flex items-center gap-3"
			>
				<span class="text-red-500 text-sm font-medium">{{ errorMessage }}</span>
				<button
					@click="errorMessage = null"
					class="ml-auto text-red-500 hover:text-red-400"
				>
					✕
				</button>
			</div>

			<div v-if="fetchingUser" class="flex flex-col items-center py-20">
				<div class="animate-spin rounded-full h-8 w-8 border-t-2 border-white mb-4"></div>
				<p class="text-gray-400">Verifying connection...</p>
			</div>

			<div v-else-if="!githubConnected" class="flex flex-col items-center py-10 text-center">
				<div class="bg-gray-900 p-6 rounded-full mb-6">
					<svg class="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24">
						<path
							d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
						/>
					</svg>
				</div>
				<h3 class="text-xl font-medium text-white mb-2">Connect your GitHub</h3>
				<p class="text-gray-400 mb-8 max-w-sm">
					We need permission to fetch your repositories and profile data to set up your
					marketplace account.
				</p>
				<Button variant="solid" class="w-full py-6" @click="redirectToGitHub">
					Authorize GitHub
				</Button>
			</div>

			<div v-else>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<FormControl
						label="Name"
						v-model="form.publisher_name"
						placeholder="Your Name"
					/>
					<FormControl
						type="select"
						label="Type"
						v-model="form.publisher_type"
						:options="[
							{ label: 'Organization', value: 'Organization' },
							{ label: 'Individual', value: 'Individual' },
						]"
					/>

					<div v-if="form.publisher_type === 'Organization'" class="md:col-span-2">
						<FormControl
							label="Company Name"
							v-model="form.company_name"
							placeholder="Your Company Ltd"
						/>
					</div>

					<FormControl
						label="Website"
						v-model="form.website"
						placeholder="https://example.com"
					/>
					<FormControl label="Email from GitHub" v-model="form.contact_email" />

					<div class="md:col-span-2 mt-2">
						<label class="block text-sm font-medium text-gray-400 mb-2">Logo</label>
						<div class="flex items-center gap-4">
							<div
								v-if="logoPreview"
								class="w-16 h-16 rounded border border-gray-700 overflow-hidden bg-gray-900"
							>
								<img :src="logoPreview" class="w-full h-full object-cover" />
							</div>
							<Button @click="showFileUploader = true">
								{{ form.logo_file ? "Change Logo" : "Attach Logo" }}
							</Button>
						</div>
					</div>
				</div>

				<div class="mt-10 flex flex-col gap-3">
					<Button
						variant="solid"
						class="w-full py-6"
						:loading="submitting"
						@click="submitForm"
					>
						Complete Setup
					</Button>
				</div>
			</div>

			<FileUploader
				v-if="showFileUploader"
				:show="showFileUploader"
				@close="showFileUploader = false"
				@success="handleLogoUpload"
			/>
		</div>
	</div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";
import { FormControl, Button, FileUploader, createResource, call } from "frappe-ui";
import { session } from "@/data/session";
import { useRouter } from "vue-router";
import { publisherState } from "@/router";

const router = useRouter();
const showFileUploader = ref(false);
const logoPreview = ref(null);
const submitting = ref(false);
const fetchingUser = ref(true);
const githubConnected = ref(false);
const errorMessage = ref(null);

const form = reactive({
	user: session.user,
	publisher_name: "",
	publisher_type: "Individual",
	company_name: "",
	website: "",
	contact_email: "",
	logo_file: null,
});

// 1. Check connection
async function checkConnection() {
	try {
		const isConnected = await call("marketplace.api.github.check_if_connected");
		if (isConnected) {
			githubConnected.value = true;
			userResource.fetch();
		} else {
			githubConnected.value = false;
			fetchingUser.value = false;
		}
	} catch (e) {
		githubConnected.value = false;
		fetchingUser.value = false;
	}
}

// 2. Fetch profile data
const userResource = createResource({
	url: "marketplace.api.github.get_github_profile_data",
	onSuccess(data) {
		form.publisher_name = data.name || data.login || "";
		form.contact_email = data.email || session.user;
		form.company_name = data.company || "";
		form.website = data.blog || "";
		logoPreview.value = data.avatar_url;
		fetchingUser.value = false;
	},
	onError(err) {
		errorMessage.value = "Connected but failed to fetch profile. Try re-connecting.";
		fetchingUser.value = false;
	},
});

// 3. START OAUTH FLOW
async function redirectToGitHub() {
	try {
		const authUrl = await call("marketplace.api.github.get_github_auth_url");
		if (authUrl) {
			window.location.href = authUrl;
		}
	} catch (e) {
		errorMessage.value = "Could not initiate GitHub connection.";
	}
}

function handleLogoUpload(file) {
	form.logo_file = file;
	logoPreview.value = file.file_url;
	showFileUploader.value = false;
}

async function submitForm() {
	if (form.publisher_type === "Organization" && !form.company_name) {
		errorMessage.value = "Company Name is required for Organizations.";
		return;
	}

	submitting.value = true;
	try {
		await call("frappe.client.insert", {
			doc: {
				doctype: "Marketplace Publisher",
				publisher_name: form.publisher_name,
				publisher_type: form.publisher_type,
				company_name: form.company_name,
				website: form.website,
				contact_email: form.contact_email,
				logo: form.logo_file ? form.logo_file.file_url : logoPreview.value,
				user: session.user,
			},
		});

		publisherState.checked = true;
		publisherState.hasProfile = true;

		router.push({ name: "MyApps" });
	} catch (error) {
		errorMessage.value = error.messages?.[0] || "Failed to save profile.";
	} finally {
		submitting.value = false;
	}
}

onMounted(() => {
	checkConnection();
});
</script>
