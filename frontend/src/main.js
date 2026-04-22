import { createApp } from "vue";

import App from "./App.vue";
import router from "./router";
import { initSocket } from "./socket";

import {
	Alert,
	Badge,
	Button,
	Card,
	Dialog,
	ErrorMessage,
	FormControl,
	Input,
	TextInput,
	frappeRequest,
	pageMetaPlugin,
	resourcesPlugin,
	setConfig,
	FrappeUI,
} from "frappe-ui";

import "./index.css";

const globalComponents = {
	Button,
	Card,
	TextInput,
	Input,
	FormControl,
	ErrorMessage,
	Dialog,
	Alert,
	Badge,
};

const app = createApp(App);

setConfig("resourceFetcher", frappeRequest);

app.use(router);
app.use(pageMetaPlugin);
app.use(FrappeUI);

const socket = initSocket();
app.config.globalProperties.$socket = socket;

for (const key in globalComponents) {
	app.component(key, globalComponents[key]);
}

if (import.meta.env.DEV) {
	frappeRequest({
		url: "/api/method/marketplace.www.dashboard.index.get_context_for_dev",
	}).then((values) => {
		for (let key in values) {
			window[key] = values[key];
		}
	});
}

app.mount("#app");
