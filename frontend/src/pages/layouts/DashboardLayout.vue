<template>
	<div class="flex h-screen w-screen overflow-hidden bg-gray-100 dark:bg-gray-950">
		<Sidebar :header="sidebarConfig.header" :sections="sidebarConfig.sections" />
		<div class="flex flex-1 flex-col overflow-hidden bg-white dark:bg-gray-900">
			<header class="border-b border-gray-200 dark:border-gray-800 px-5 py-3">
				<Breadcrumbs :items="breadcrumbItems" />
			</header>
			<main class="flex-1 overflow-y-auto p-6">
				<router-view />
			</main>
		</div>
	</div>
</template>

<script setup lang="ts">
import { reactive, computed, ref, onMounted } from "vue";
import { Sidebar, Breadcrumbs, createResource } from "frappe-ui";
import { useRoute } from "vue-router";
import { session } from "../../data/session";
import { LayoutDashboard, PlusCircle, UserCircle, LogOut, Moon } from "lucide-vue-next";

const route = useRoute();

const breadcrumbItems = computed(() => {
	const items: { label: string; route: { name: string; params?: any } }[] = [
		{
			label: "App Dashboard",
			route: { name: "MyApps" },
		},
	];

	if (route.name === "MyApps") {
		items.push({
			label: "My Apps",
			route: { name: "MyApps" },
		});
	} else if (route.name === "AppDetails") {
		items.push({
			label: "My Apps",
			route: { name: "MyApps" },
		});

		items.push({
			label: String(route.params.app_name ?? "App"),
			route: {
				name: "AppDetails",
				params: { app_name: route.params.app_name },
			},
		});
	} else if (route.name === "CreateApp") {
		items.push({
			label: "Create App",
			route: { name: "CreateApp" },
		});
	} else if (route.name === "ManageApp") {
		items.push({
			label: "Create App",
			route: { name: "CreateApp" },
		});
		items.push({
			label: String(route.params.appName ?? "Repository"),
			route: {
				name: "ManageApp",
				params: { appName: route.params.appName },
			},
		});
	}

	return items;
});

function toggleTheme() {
	const currentTheme = document.documentElement.getAttribute("data-theme");
	const newTheme = currentTheme === "dark" ? "light" : "dark";
	document.documentElement.setAttribute("data-theme", newTheme);
}

const publisherName = ref("Publisher");
const publisherResource = createResource({
	url: "frappe.client.get_value",
	params: {
		doctype: "Marketplace Publisher",
		filters: { user: session.user },
		fieldname: ["publisher_name"],
	},
	auto: false,
});

onMounted(async () => {
	try {
		const res = await publisherResource.fetch();
		if (res?.publisher_name) {
			publisherName.value = res.publisher_name;
			sidebarConfig.header.subtitle = res.publisher_name;
		}
	} catch (e) {
		console.error("Failed to fetch publisher", e);
	}
});

const sidebarConfig = reactive({
	header: {
		title: "Marketplace",
		subtitle: publisherName.value,
		logo: "",
		menuItems: [
			{
				label: "Toggle Theme",
				icon: Moon,
				onClick: toggleTheme,
			},
			{
				label: "Logout",
				icon: LogOut,
				onClick: () => session.logout.submit(),
			},
		],
	},
	sections: [
		{
			label: "Publishing",
			items: [
				{
					label: "My Apps",
					to: "/dashboard/my-apps",
					icon: LayoutDashboard,
				},
				{
					label: "Create New App",
					to: "/dashboard/create-app",
					icon: PlusCircle,
				},
			],
		},
		{
			label: "Account",
			collapsible: true,
			items: [
				{
					label: "Publisher Profile",
					to: "/dashboard/publisher-profile",
					icon: UserCircle,
				},
			],
		},
	],
});
</script>
