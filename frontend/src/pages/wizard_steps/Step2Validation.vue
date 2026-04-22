<template>
	<div class="space-y-8 animate-in fade-in zoom-in duration-500">
		<div class="text-center py-10">
			<h2 class="text-2xl font-bold mb-2 tracking-tight text-gray-900 dark:text-white">
				Technical Validation
			</h2>
			<p class="text-gray-500 dark:text-gray-400">
				Validating release:
				<span class="font-mono text-sm text-gray-900 dark:text-white">
					{{ form.app_release_id }}
				</span>
			</p>
			<p v-if="hash" class="text-xs text-gray-500 mt-2">
				Commit:
				<span class="font-mono">{{ hash.substring(0, 7) }}</span>
			</p>
		</div>
		<div
			class="border border-gray-200 dark:border-gray-800 rounded-3xl overflow-hidden bg-white dark:bg-gray-900"
		>
			<div
				v-for="check in automatedChecks"
				:key="check.id"
				class="flex items-center justify-between px-10 py-6 border-b border-gray-200 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-800/40 transition-colors"
			>
				<div class="flex items-center gap-4">
					<div
						:class="[
							check.status === 'running'
								? 'animate-pulse bg-blue-500'
								: check.status === 'pass'
								? 'bg-green-500'
								: check.status === 'fail'
								? 'bg-red-500'
								: 'bg-gray-300 dark:bg-gray-700',
							'w-2 h-2 rounded-full transition-all duration-500',
						]"
					></div>
					<span class="font-medium text-gray-800 dark:text-gray-200">{{
						check.label
					}}</span>
				</div>

				<div class="flex items-center gap-3">
					<LoadingIndicator v-if="check.status === 'running'" class="w-4 h-4" />
					<FeatherIcon
						v-else-if="check.status === 'pass'"
						name="check-circle"
						class="w-5 h-5 text-green-500"
					/>
					<FeatherIcon
						v-else-if="check.status === 'fail'"
						name="x-circle"
						class="w-5 h-5 text-red-500"
					/>
					<span v-else class="text-xs text-gray-400 uppercase font-bold tracking-widest"
						>Waiting</span
					>
				</div>
			</div>
		</div>

		<div
			v-if="ciStatus === 'Failed'"
			class="mt-4 p-4 bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-900 rounded-xl"
		>
			<p class="text-xs font-bold text-red-500 uppercase mb-2">Build Logs</p>
			<pre class="text-xs text-red-600 dark:text-red-300 font-mono whitespace-pre-wrap">{{
				validationLogs || "No logs available"
			}}</pre>
		</div>

		<div
			class="mt-12 p-6 border border-gray-200 dark:border-gray-800 rounded-2xl bg-gray-50 dark:bg-gray-900 flex items-start gap-4"
		>
			<p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed italic">
				The validation process checks your hooks.py for required dependencies and executes
				automated benchmarks. You will be able to proceed once the build completes
				successfully.
			</p>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { LoadingIndicator, FeatherIcon, call } from "frappe-ui";

const props = defineProps(["form"]);
const emit = defineEmits(["validated"]);

const ciStatus = ref("Pending");
const validationLogs = ref("");
const hash = ref("");
let pollInterval = null;

const automatedChecks = computed(() => [
	{ id: "repo", label: "GitHub Repository Connection", status: "pass" },
	{ id: "hooks", label: "Dependency Graph (hooks.py)", status: "pass" },
	{
		id: "ci",
		label: "Marketplace CI Build Pipeline",
		status:
			ciStatus.value === "Passed"
				? "pass"
				: ciStatus.value === "Failed"
				? "fail"
				: ciStatus.value === "Running"
				? "running"
				: "waiting",
	},
]);

async function fetchStatus() {
	if (!props.form.app_release_id) return;

	try {
		const data = await call("frappe.client.get_value", {
			doctype: "App Release",
			filters: { name: props.form.app_release_id },
			fieldname: ["ci_status", "validation_logs", "hash"],
		});

		if (data) {
			ciStatus.value = data.ci_status;
			validationLogs.value = data.validation_logs;
			hash.value = data.hash || "";

			if (ciStatus.value === "Passed") {
				emit("validated", true);
				stopPolling();
			} else if (ciStatus.value === "Failed") {
				emit("validated", false);
				stopPolling();
			}
		}
	} catch (e) {
		console.error("Error polling status:", e);
	}
}

function stopPolling() {
	if (pollInterval) {
		clearInterval(pollInterval);
		pollInterval = null;
	}
}

onMounted(() => {
	fetchStatus();
	pollInterval = setInterval(fetchStatus, 3000);
});

onUnmounted(() => {
	stopPolling();
});
</script>
