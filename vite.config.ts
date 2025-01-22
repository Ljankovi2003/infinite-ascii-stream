import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  server: {
    host: "::", // Allow all IP addresses
    port: 8080,
    proxy: {
      '/api': {
        target:
          mode === 'development' ? 'http://127.0.0.1:5000' : '/api', // Local Flask server in dev, or remote API in prod
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''), // Remove /api prefix before forwarding to Flask
      },
    },
  },
  plugins: [
    react(),
    mode === 'development' &&
      componentTagger(),
  ].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}));
