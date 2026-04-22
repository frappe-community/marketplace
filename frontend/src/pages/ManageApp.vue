<template>
	<div class="flex h-screen flex-col bg-white dark:bg-gray-950">
		<header
			class="flex h-16 items-center justify-between border-b bg-white px-6 dark:bg-gray-900"
		>
			<div class="flex items-center gap-4">
				<div>
					<p class="text-[10px] font-bold uppercase tracking-widest text-gray-500">
						Submit App
					</p>
					<h1 class="text-lg font-bold text-gray-900 dark:text-white leading-none">
						{{ form.app_title || "New Application" }}
					</h1>
				</div>
			</div>

			<nav class="hidden flex-1 justify-center md:flex">
				<div class="flex items-center gap-8">
					<div
						v-for="(label, index) in ['Details', 'Validation', 'Review']"
						:key="label"
						class="flex items-center gap-3"
					>
						<Badge
							:variant="currentStep >= index + 1 ? 'solid' : 'subtle'"
							theme="gray"
							size="lg"
							class="h-6 w-6 rounded-full px-0 flex justify-center"
						>
							{{ index + 1 }}
						</Badge>
						<span
							:class="[
								'text-sm font-medium',
								currentStep === index + 1
									? 'text-gray-900 dark:text-white'
									: 'text-gray-400',
							]"
						>
							{{ label }}
						</span>
					</div>
				</div>
			</nav>

			<div class="flex items-center gap-3">
				<div
					v-if="isValidating"
					class="flex items-center gap-2 pr-4 text-xs text-gray-500"
				>
					<LoadingIndicator class="w-4 h-4" />
					<span>Verifying...</span>
				</div>
				<Button
					v-if="currentStep > 1"
					variant="ghost"
					label="Back"
					@click="currentStep--"
				/>
				<Button
					variant="solid"
					:loading="processing"
					:disabled="isNextDisabled"
					:label="currentStep === 3 ? 'Finish Submission' : 'Continue'"
					@click="handleContinue"
				/>
			</div>
		</header>

		<main class="flex-1 overflow-y-auto">
			<div class="mx-auto max-w-6xl px-6 py-10">
				<div v-if="validationError" class="mb-8">
					<Alert
						theme="red"
						:title="validationError"
						:dismissable="true"
						v-model="showAlert"
						@close="validationError = ''"
					>
						<template #description>
							<span class="block mt-1">
								Please verify your repository settings and Frappe version
								compatibility in the Basic Info section.
							</span>
						</template>
					</Alert>
				</div>

				<div
					v-if="repoMeta.loading"
					class="flex h-64 flex-col items-center justify-center gap-4"
				>
					<LoadingIndicator class="h-8 w-8" />
					<p class="text-sm text-gray-500">Fetching repository info...</p>
				</div>

				<div v-else>
					<Step1Details
						v-if="currentStep === 1"
						:form="form"
						:branches="repoMeta.branches"
						:dependencies="repoMeta.dependencies"
						:loadingMeta="repoMeta.loading"
						:frappeRequirement="repoMeta.frappe_requirement"
					/>

					<div v-if="currentStep === 2" class="mx-auto max-w-3xl">
						<Step2Validation :form="form" @validated="handleValidationUpdate" />
					</div>

					<div v-if="currentStep === 3" class="mx-auto max-w-3xl">
						<Step3Review :form="form" />
					</div>
				</div>
			</div>
		</main>
	</div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Alert, Button, Badge, LoadingIndicator, FeatherIcon, call } from "frappe-ui";

import Step1Details from "./wizard_steps/Step1Details.vue";
import Step2Validation from "./wizard_steps/Step2Validation.vue";
import Step3Review from "./wizard_steps/Step3Review.vue";

const processing = ref(false);
const isValidating = ref(false);
const validationPassed = ref(false);
const validationError = ref("");
const showAlert = ref(false);

const route = useRoute();
const router = useRouter();

const currentStep = ref(Number(route.query.step) || 1);

watch(currentStep, (step) => {
	router.replace({
		query: { ...route.query, step },
	});
});

const form = reactive({
	app_name: (route.query.repo_name as string) || "",
	app_title: (route.query.repo_name as string) || "",
	repo_url: (route.query.repo_url as string) || "",
	description: (route.query.repo_description as string) || "",
	branch: "",
	logo: null,
	app_release_id: (route.query.app_release_id as string) || "",
	versions: [{ version: "", branch: "" }],
});

watch(
	() => form.app_release_id,
	(id) => {
		if (id) router.replace({ query: { ...route.query, app_release_id: id } });
	}
);

const repoMeta = reactive({
	branches: [],
	dependencies: [],
	loading: false,
	frappe_requirement: undefined as string | undefined,
});

const repoData = ref({});

watch(
	() => ({
		repo_url: form.repo_url,
		app_name: form.app_name,
		branch: form.branch,
	}),
	() => {
		validationPassed.value = false;
		validationError.value = "";
		showAlert.value = false;
	},
	{ deep: true }
);

onMounted(async () => {
	if (!form.repo_url) {
		router.replace({ name: "CreateApp" });
		return;
	}
	repoMeta.loading = true;
	try {
		const data = await call("marketplace.api.github.fetch_repo_info", {
			repo_url: form.repo_url,
		});
		repoData.value = data.raw_github_data || {};
		if (data.metadata) {
			form.app_name = data.metadata.app_name || form.app_name;
			form.app_title = data.metadata.app_title || form.app_title;
			form.description = data.metadata.app_description || form.description;
			repoMeta.frappe_requirement = data.metadata.frappe_version_requirement;
		}
		if (data.default_branch && form.versions.length)
			form.versions[0].branch = data.default_branch;
		repoMeta.branches = data.branches || [];
		repoMeta.dependencies = data.metadata?.dependencies || [];
	} finally {
		repoMeta.loading = false;
	}
});

async function checkCompatibility() {
	showAlert.value = false;
	if (!repoMeta.frappe_requirement) {
		validationPassed.value = true;
		return true;
	}

	const selectedVersion = form.versions[0]?.version;
	if (!selectedVersion) {
		validationError.value = "Please select a Frappe version.";
		showAlert.value = true;
		return false;
	}

	isValidating.value = true;
	try {
		const isCompatible = await call("marketplace.api.github.check_version_compatibility", {
			required_range: repoMeta.frappe_requirement,
			user_version: selectedVersion,
		});

		if (!isCompatible) {
			validationError.value = `Incompatible Version: This app requires Frappe ${repoMeta.frappe_requirement}.`;
			validationPassed.value = false;
			showAlert.value = true;
			return false;
		}

		validationError.value = "";
		validationPassed.value = true;
		return true;
	} catch (error: any) {
		validationError.value = error.message || "Compatibility check failed.";
		showAlert.value = true;
		return false;
	} finally {
		isValidating.value = false;
	}
}

async function initializeApp() {
	if (form.app_release_id) {
		return true;
	}
	showAlert.value = false;
	try {
		const res = await call("marketplace.api.setup_wizard.initialize_app_step_1", {
			form_data: JSON.stringify(form),
			repo_data: repoData.value,
		});
		form.app_release_id = res.app_release;
		return true;
	} catch (error: any) {
		let errorMessage = "An error occurred while creating the app record.";
		if (error.messages && error.messages.length > 0) {
			errorMessage = error.messages[0];
		} else if (error.message) {
			errorMessage = error.message;
		}

		validationError.value = errorMessage;
		showAlert.value = true;
		window.scrollTo({ top: 0, behavior: "smooth" });
		return false;
	}
}

async function handleContinue() {
	if (currentStep.value === 1) {
		const compatible = await checkCompatibility();
		if (!compatible) return;

		if (form.app_release_id) {
			validationPassed.value = false;
			currentStep.value = 2;
			return;
		}

		processing.value = true;
		try {
			const success = await initializeApp();
			if (success) {
				validationPassed.value = false;
				currentStep.value = 2;
				validationError.value = "";
				showAlert.value = false;
			}
		} finally {
			processing.value = false;
		}
		return;
	}

	if (currentStep.value === 2 && validationPassed.value) {
		currentStep.value = 3;
		return;
	}

	if (currentStep.value === 3) {
		processing.value = true;
		try {
			await call("marketplace.api.setup_wizard.finalize_submission", {
				app_release_id: form.app_release_id,
			});
			router.push({ name: "MyApps" });
		} finally {
			processing.value = false;
		}
	}
}

const isNextDisabled = computed(() => {
	if (currentStep.value === 1) {
		return (
			!form.app_name || !form.versions[0]?.version || processing.value || isValidating.value
		);
	}
	if (currentStep.value === 2) return !validationPassed.value || processing.value;
	return processing.value;
});

function handleValidationUpdate(status: boolean) {
	validationPassed.value = status;
}
</script>
