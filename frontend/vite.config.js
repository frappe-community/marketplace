import path from "node:path";
import vue from "@vitejs/plugin-vue";
import frappeui from "frappe-ui/vite";
import { defineConfig } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		frappeui({
			frappeProxy: {
				port: 8080,
				rules: {
					"^/(api|login|logout|assets|files|socket.io)": {
						target: "http://newmktplace.localhost",
						changeOrigin: true,
						ws: true,
					},
				},
			},
			jinjaBootData: true,
			lucideIcons: true,
			buildConfig: {
				outDir: "../marketplace/public/marketplace",
				indexHtmlPath: "../marketplace/www/dashboard/index.html",
				emptyOutDir: true,
				sourcemap: true,
			},
		}),
		vue(),
	],
	build: {
		chunkSizeWarningLimit: 1500,
		outDir: "../marketplace/public/marketplace",
		emptyOutDir: true,
		target: "es2015",
		sourcemap: true,
	},
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "src"),
			"tailwind.config.js": path.resolve(__dirname, "tailwind.config.js"),
		},
	},
	optimizeDeps: {
		include: ["feather-icons", "showdown", "highlight.js/lib/core", "interactjs"],
	},
	server: {
		allowedHosts: true,
	},
});
