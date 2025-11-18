import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "node:path";

const apiProxyTarget = process.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    host: "0.0.0.0",
    proxy: {
      "/objects": apiProxyTarget,
      "/stats": apiProxyTarget,
      "/health": apiProxyTarget,
      "/ready": apiProxyTarget
    }
  },
  build: {
    outDir: resolve(__dirname, "../astro_analysis_service/static/app"),
    emptyOutDir: true
  },
  base: "/app/"
});
