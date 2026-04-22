<template>
	<div class="space-y-10 animate-in fade-in slide-in-from-bottom-5 duration-700">
		<section class="border border-gray-200 rounded-3xl p-8">
			<div class="flex items-start gap-8">
				<div
					class="w-24 h-24 rounded-2xl bg-gray-100 border border-gray-200 flex-shrink-0 flex items-center justify-center overflow-hidden"
				>
					<img v-if="form.logo" :src="form.logo" class="w-full h-full object-cover" />
					<FeatherIcon v-else name="image" class="w-8 h-8 text-gray-400" />
				</div>
				<div class="space-y-4 flex-1">
					<div>
						<h2 class="text-2xl font-bold tracking-tight text-gray-900">
							{{ form.app_title }}
						</h2>
						<p class="text-gray-500 mt-1">{{ form.description }}</p>
					</div>
					<div class="flex items-center gap-6">
						<div class="flex items-center gap-2">
							<FeatherIcon name="user" class="w-4 h-4 text-gray-400" />
							<span class="text-sm text-gray-600">Publisher Verified</span>
						</div>
						<div class="flex items-center gap-2">
							<FeatherIcon name="github" class="w-4 h-4 text-gray-400" />
							<span class="text-sm text-gray-600">Open Source</span>
						</div>
					</div>
				</div>
			</div>
		</section>

		<section class="space-y-4">
			<h3 class="text-xs font-bold uppercase tracking-widest text-gray-500">
				Supported Versions
			</h3>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<div
					v-for="v in form.versions"
					:key="v.version"
					class="flex items-center justify-between p-4 bg-gray-50 border border-gray-200 rounded-xl"
				>
					<div class="flex items-center gap-3">
						<Badge theme="blue" variant="subtle">{{
							v.version?.value || v.version
						}}</Badge>
						<span class="text-gray-500 font-mono text-sm">/ {{ v.branch }}</span>
					</div>
					<FeatherIcon name="check" class="w-4 h-4 text-green-500" />
				</div>
			</div>
		</section>

		<div class="p-6 bg-blue-50 border border-blue-200 rounded-2xl flex gap-4">
			<FeatherIcon name="info" class="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" />
			<div class="space-y-1">
				<p class="text-sm text-blue-700 font-medium">Ready for Submission</p>
				<p class="text-xs text-blue-600 leading-relaxed">
					By clicking finish, your app will be sent to the Marketplace team for approval.
					Technical validation has already confirmed your repository structure is
					compatible.
				</p>
			</div>
		</div>
	</div>
</template>

<script setup>
import { FeatherIcon, Badge } from "frappe-ui";
const props = defineProps(["form"]);
</script>
